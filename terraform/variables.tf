variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "ami_id" {
  type    = string
  default = "ami-0c7217cdde317cfec"
}

variable "allowed_ip_cidr" {
  type    = string
  default = "192.168.1.100/32"
}