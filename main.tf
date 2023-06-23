data "azurerm_subnet" "example" {
  name = "internal"
  virtual_network_name = "network-tp4"
  resource_group_name = "ADDA84-CTP"
}

resource "azurerm_public_ip" "my_terraform_public_ip" {
  name                = "20220090-IP"
  location            = "francecentral"
  resource_group_name = data.azurerm_subnet.example.resource_group_name
  allocation_method   = "Dynamic"
}

resource "azurerm_network_interface" "my_terraform_nic" {
  name                = "20220090-NIC"
  location            = "francecentral"
  resource_group_name = data.azurerm_subnet.example.resource_group_name

  ip_configuration {
    name                          = data.azurerm_subnet.example.name
    subnet_id                     = data.azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.my_terraform_public_ip.id
  }
}

resource "tls_private_key" "example_ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "azurerm_linux_virtual_machine" "my_terraform_vm" {
  name                  = "devops-20220090"
  location              = "francecentral"
  resource_group_name   = data.azurerm_subnet.example.resource_group_name
  network_interface_ids = [azurerm_network_interface.my_terraform_nic.id]
  size                  = "Standard_D2s_v3"

  os_disk {
    name                 = "20220090O-sDisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }

  computer_name                   = "20220090-VM"
  admin_username                  = "devops"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "devops"
    public_key = tls_private_key.example_ssh.public_key_openssh
  }
}