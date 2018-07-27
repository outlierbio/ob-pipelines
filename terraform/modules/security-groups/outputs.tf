# General
output "default" {
  value = "${aws_default_security_group.default.id}"
}

# Public inbound
output "public_ssh" {
  value = "${aws_security_group.public_ssh.id}"
}

output "public_http" {
  value = "${aws_security_group.public_http.id}"
}

output "public_https" {
  value = "${aws_security_group.public_https.id}"
}

output "public_web" {
  value = "${aws_security_group.public_web.id}"
}
