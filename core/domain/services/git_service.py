import os
import subprocess
from git import Repo, exc

class GitService:
    @staticmethod
    def clone_repository_with_submodules(repo_url, repo_name=None, branch=None):
        """
        Clona un repositorio GitHub con sus submódulos.
        Si el repositorio ya existe, actualiza sus submódulos.
        """
        base_dir = os.path.join(os.getcwd(), "repositories", "clone")
        os.makedirs(base_dir, exist_ok=True)

        if not repo_name:
            repo_name = repo_url.rstrip('/').split("/")[-1]
            if repo_name.endswith(".git"):
                repo_name = repo_name[:-4]

        repo_path = os.path.join(base_dir, repo_name)

        if os.path.exists(repo_path):
            # Repositorio ya existe: actualizar submódulos
            try:
                repo = Repo(repo_path)
                repo.git.submodule('update', '--init', '--recursive')
            except exc.GitCommandError as e:
                raise RuntimeError(f"Error al actualizar submódulos: {e}")
        else:
            # Clonar con submódulos
            cmd = ["git", "clone", "--recurse-submodules"]
            if branch:
                cmd.extend(["-b", branch])
            cmd.extend([repo_url, repo_path])

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                repo = Repo(repo_path)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Error al clonar el repositorio: {e.stderr}")

        # Obtener información del repositorio y submódulos
        try:
            submodules = []
            for submodule in repo.submodules:
                submodules.append({
                    "name": submodule.name,
                    "path": submodule.path,
                    "url": submodule.url
                })

            return {
                "repo_name": repo_name,
                "repo_url": repo_url,
                "branch": branch or repo.active_branch.name,
                "commit_hash": repo.head.commit.hexsha,
                "submodules": submodules,
                "clone_path": repo_path
            }
        except Exception as e:
            raise RuntimeError(f"Error al obtener información del repositorio: {str(e)}")
