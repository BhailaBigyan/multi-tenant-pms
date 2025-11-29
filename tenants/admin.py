from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'schema_name',
        'tenant_code',
        'is_active',
        'expires_at',
        'auto_disable',
        'created_on',
    )
    list_filter = ('is_active', 'auto_disable', 'created_on', 'expires_at')
    search_fields = ('name', 'schema_name', 'tenant_code')
    list_editable = ('is_active', 'auto_disable', 'expires_at')
    actions = ['activate_tenants', 'deactivate_tenants']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'schema_name', 'tenant_code', 'is_active', 'auto_disable', 'expires_at', 'disabled_at')
        }),
        ('Access Control', {
            'fields': ('access_pin',)
        }),
        ('Database Configuration', {
            'fields': ('subdomain', 'db_name', 'db_user', 'db_password', 'db_host', 'db_port'),
            'classes': ('collapse',)
        }),
        ('Advanced', {
            'fields': ('auto_create_schema', 'auto_drop_schema', 'created_on'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_on', 'disabled_at')

    @admin.action(description="Deactivate selected tenants")
    def deactivate_tenants(self, request, queryset):
        updated = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, f"Deactivated {updated} tenant(s).")

    @admin.action(description="Activate selected tenants")
    def activate_tenants(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True, disabled_at=None)
        self.message_user(request, f"Activated {updated} tenant(s).")


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')

