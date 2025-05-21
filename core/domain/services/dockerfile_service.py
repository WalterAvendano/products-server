# Ya no es necesario este archivo si usas la clase DockerfileService dentro de dockerfile_models.py
# Pero si quieres mantenerlo separado, asegúrate que la función build_odoo_dockerfile
# use solo odoo_version y filename, y que no intente acceder a atributos eliminados.

# Si decides mantenerlo, actualízalo así:

class DockerfileService:
    @staticmethod
    def build_odoo_dockerfile(odoo_data) -> str:
        version = odoo_data.odoo_version
        content = f"""FROM odoo:{version}
COPY ./enterprise /opt/odoo/enterprise
RUN chown -R odoo:odoo /opt/odoo/enterprise
WORKDIR /opt/odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf", "-d", "odoo{version}"]
"""
        return content

    @staticmethod
    def build_generic_dockerfile(data) -> str:
        # Mantener implementación original para genéricos
        pass
