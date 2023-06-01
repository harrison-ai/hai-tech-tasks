resource "aws_dynamodb_table" "this" {
  name           = var.name
  billing_mode   = var.billing_mode
  hash_key       = var.hash_key_name
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  attribute {
    name = var.hash_key_name
    type = var.hash_key_type
  }
}
