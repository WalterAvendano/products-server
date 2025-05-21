from pydantic import BaseModel

class OdooDockerfile(BaseModel):
    odoo_version: str  # Nueva propiedad para versión dinámica
    filename: str      # Necesario para guardar el archivo

class GenericDockerfile(BaseModel):
    base_image: str
    maintainer_name: str
    maintainer_email: str
    system_packages: list
    commands: list
    expose_ports: list
    working_dir: str
    user: str
    volumes: list
    filename: str

class DockerfileService:

    @staticmethod
    def build_odoo_dockerfile(odoo_data: OdooDockerfile) -> str:
        """
        Genera Dockerfile para Odoo con estructura fija y versión dinámica.
        """
        version = odoo_data.odoo_version
        content = f"""FROM odoo:{version}
COPY ./enterprise /opt/odoo/enterprise
RUN chown -R odoo:odoo /opt/odoo/enterprise
WORKDIR /opt/odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf", "-d", "odoo{version}"]
"""
        return content

    @staticmethod
    def build_generic_dockerfile(data: GenericDockerfile) -> str:
        dockerfile = [
            f"FROM {data.base_image}",
            f'LABEL maintainer="{data.maintainer_name} <{data.maintainer_email}>"',
            f"RUN apt-get update && apt-get install -y {' '.join(data.system_packages)}"
        ]
        for cmd in data.commands:
            dockerfile.append(f"RUN {cmd}")
        for port in data.expose_ports:
            dockerfile.append(f"EXPOSE {port}")
        dockerfile.append(f"WORKDIR {data.working_dir}")
        dockerfile.append(f"USER {data.user}")
        for vol in data.volumes:
            dockerfile.append(f'VOLUME ["{vol}"]')
        return "\n".join(dockerfile)
