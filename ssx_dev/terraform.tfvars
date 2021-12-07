aws_region = "eu-central-1"
# aws_access_key    = "your aws access key"
# aws_secret_key    = "your aws secret key"

# these are zones and subnets examples
availability_zones = ["eu-central-1a", "eu-central-1b"]
public_subnets     = ["10.10.100.0/24", "10.10.101.0/24"]
private_subnets    = ["10.10.0.0/24", "10.10.1.0/24"]

# these are used for tags
app_name          = "ssx-odoo-app"
app_environment   = "devenv"
hosted_zone_id    = "Z1PSEXSC6MXGQ4"
database_fqdn     = "ssx-odoo-db.sysloggh.com"
loadbalancer_fqdn = "ssx-odoo.sysloggh.com"
odoo_db_name      = "odoo_db"
odoo_user         = "odoo"
odoo_db_password  = "secretpassword"
cloudwatch_group = "ssx-odoo-app"