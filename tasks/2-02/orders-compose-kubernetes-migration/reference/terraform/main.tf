terraform {
  required_providers {
    helm = { source = "hashicorp/helm", version = "2.17.0" }
  }
}
variable "kubeconfig" {
  type = string
  description = "本题隔离K3s集群的kubeconfig，不可指向生产集群"
  default = "/etc/rancher/k3s/k3s.yaml"
}
provider "helm" {
  kubernetes { config_path = var.kubeconfig }
}
resource "helm_release" "webapp" {
  name = "webapp"
  namespace = "alecn"
  create_namespace = true
  chart = "${path.module}/../helm/webapp-chart"
}
output "release_name" { value = helm_release.webapp.name }
