# TP4 20220090 Mathis Da Cruz 

## Objectifs

* Créer une machine virtuelle Azure (VM) avec une adresse IP publique dans un réseau existant ( network-tp4 )
* Utiliser Terraform
* Se connecter à la VM avec SSH
* Comprendre les différents services Azure (ACI vs. AVM)

---

## 1. Créer une machine virtuelle Azure

Provider.tf

Configuration de base de Terraform avec le fournisseur Azure (azurerm) et le subscription_id.

```
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "765266c6-9a23-4638-af32-dd1e32613047"
}
```

Main.tf


* Création d'une machine virtuelle Azure avec une adresse IP publique dans le réseau network-tp4 et le groupe de ressources ADDA84-CTP. 
* Utilise les données du sous-réseau internal pour définir les valeurs des ressources.
* Génère une clé privée SSH avec une longueur de 4096 bits.

```
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
```

## 2. Utiliser Terraform

1. Initialise Terraform

```
terraform init
```

2. Affiche le plan d'exécution pour créer les ressources 

```
terraform plan
```

3. Demande confirmation avant de les créer

```
terraform apply
```

---

## 3. Connection à la VM avec SSH

Output.tf

Ces outputs permettent de récupérer les valeurs suivantes après le déploiement :
* resource_group_name: le nom du groupe de ressources (ADDA84-CTP)
* public_ip_address: l'adresse IP publique de la machine virtuelle Linux déployée
* tls_private_key: la clé privée SSH au format PEM générée par Terraform. Cette sortie est secrète, ce qui signifie que sa valeur ne sera pas affichée dans les journaux Terraform.

```
output "resource_group_name" {
  value = data.azurerm_subnet.example.resource_group_name
}

output "public_ip_address" {
  value = azurerm_linux_virtual_machine.my_terraform_vm.public_ip_address
}

output "tls_private_key" {
  value     = tls_private_key.example_ssh.private_key_pem
  sensitive = true

}
```

Afficher l'adresse IP publique de la machine virtuelle déployée : 

```
terraform output public_ip_address
```

Output :

```
"20.216.180.179"
```

Redirection de la valeur de la clé privée SSH vers un fichier nommé "rsa.txt" : 

```
terraform output -raw tls_private_key > rsa.txt
```

rsa.txt

```
-----BEGIN RSA PRIVATE KEY-----
MIIJKgIBAAKCAgEA3/UEWiM1iEoMLft329l6382HSsaiTJz9LSABw1N03gyAICfw
KHM2MX2K83pUKBOevB......2KzGBnyxyoOF72Txnbg==
-----END RSA PRIVATE KEY-----
```

Commande connnexion ssh à la VM : 

```
ssh -i rsa.txt devops@20.216.180.179 cat /etc/os-release
```

* Connection à la VM à l'aide de SSH en utilisant la clé privée SSH contenue dans le fichier "rsa.txt".
* Connecté en tant qu'utilisateur "devops" à l'adresse IP publique "20.216.180.179" e
* "cat /etc/os-release" pour afficher les informations relatives à la version du système d'exploitation.

Output : 

```
NAME="Ubuntu"
VERSION="16.04.7 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.7 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
```

