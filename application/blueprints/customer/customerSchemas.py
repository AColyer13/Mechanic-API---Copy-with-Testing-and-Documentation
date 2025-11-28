"""Customer schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError, pre_load, post_load
import bcrypt
from application.models import Customer
from application.extensions import db, ma


class CustomerSchema(SQLAlchemyAutoSchema):
    """Schema for Customer model with validation."""
    
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session
        include_fk = True
        
    # Custom field validations
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=200))
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Include service tickets when needed
    service_tickets = fields.Nested('ServiceTicketSchema', many=True, dump_only=True, exclude=('customer',))
    
    @pre_load
    def process_input(self, data, **kwargs):
        """Strip whitespace and hash password before loading."""
        if isinstance(data, dict):
            # Strip whitespace from string fields
            for key, value in data.items():
                if isinstance(value, str) and key != 'password':
                    data[key] = value.strip()
            # NOTE: do NOT hash the password here — validation must run on the
            # raw password value (so length checks are enforced). Hashing is
            # performed in a post_load hook after validation.
        
        return data

    @post_load
    def hash_password(self, data, **kwargs):
        """Hash password after validation/load so validators run on raw input.

        The SQLAlchemyAutoSchema is configured with `load_instance=True`, so
        `data` may be either a dict or a model instance. Handle both cases and
        avoid double-hashing if the password already appears hashed.
        """
        # Helper to hash a raw password string
        def _hash(raw_pw):
            if not raw_pw:
                return raw_pw
            if isinstance(raw_pw, str) and raw_pw.startswith('$2'):
                # Looks already like a bcrypt hash, skip
                return raw_pw
            pw_bytes = raw_pw.encode('utf-8')
            hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
            return hashed.decode('utf-8')

        # If SQLAlchemyAutoSchema returned a model instance
        if not isinstance(data, dict):
            if hasattr(data, 'password') and data.password:
                data.password = _hash(data.password)
            return data

        # If we received a dict (rare with load_instance=True but handle it)
        if 'password' in data and data['password']:
            data['password'] = _hash(data['password'])

        return data


class LoginSchema(ma.Schema):
    """Schema for customer login - only email and password."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


# Schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Schema without service tickets and password for simpler responses
customer_simple_schema = CustomerSchema(exclude=['service_tickets', 'password'])
customers_simple_schema = CustomerSchema(many=True, exclude=['service_tickets', 'password'])

# Login schema instance
login_schema = LoginSchema()