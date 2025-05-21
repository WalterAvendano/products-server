import docker

class ContainerService:
    @staticmethod
    def list_containers(all_containers=False):
        client = docker.from_env()
        containers = client.containers.list(all=all_containers)
        result = []
        for c in containers:
            result.append({
                "id": c.id,
                "name": c.name,
                "image": c.image.tags,
                "status": c.status
            })
        return result

    @staticmethod
    def pause_container(container_id_or_name):
        client = docker.from_env()
        container = client.containers.get(container_id_or_name)
        container.pause()
        return {"id": container.id, "status": container.status}

    @staticmethod
    def unpause_container(container_id_or_name):
        client = docker.from_env()
        container = client.containers.get(container_id_or_name)
        container.unpause()
        return {"id": container.id, "status": container.status}

    @staticmethod
    def remove_container(container_id_or_name):
        client = docker.from_env()
        container = client.containers.get(container_id_or_name)
        container.stop()
        container.remove()
        return {"id": container.id, "status": "removed"}
    
    @staticmethod
    def create_container(image_name, container_name=None):
        client = docker.from_env()
        container = client.containers.run(image_name, name=container_name, detach=True)
        return {
            "id": container.id,
            "name": container.name,
            "status": container.status
        }

