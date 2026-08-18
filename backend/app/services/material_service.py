from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from backend.app.core.exceptions import NotFoundException
from backend.app.models.material import StudyMaterial
from backend.app.repositories.material_repository import StudyMaterialRepository
from backend.app.schemas.material import StudyMaterialCreate, StudyMaterialUpdate
from backend.app.services.base import BaseService


class StudyMaterialService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.material_repo = StudyMaterialRepository()

    def get_materials(
        self,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        subtopic_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[StudyMaterial], int]:
        return self.material_repo.get_multi_filtered(
            self.db,
            subject_id=subject_id,
            topic_id=topic_id,
            subtopic_id=subtopic_id,
            search=search,
            skip=skip,
            limit=limit,
        )

    def get_material(self, material_id: int) -> StudyMaterial:
        material = self.material_repo.get(self.db, id=material_id)
        if not material:
            raise NotFoundException(message=f"Study material with ID {material_id} not found.")
        return material

    def create_material(self, obj_in: StudyMaterialCreate) -> StudyMaterial:
        def _action():
            return self.material_repo.create(self.db, obj_in=obj_in)
        return self.execute_in_transaction(_action)

    def update_material(self, material_id: int, obj_in: StudyMaterialUpdate) -> StudyMaterial:
        def _action():
            material = self.get_material(material_id)
            return self.material_repo.update(self.db, db_obj=material, obj_in=obj_in)
        return self.execute_in_transaction(_action)

    def delete_material(self, material_id: int) -> None:
        def _action():
            self.get_material(material_id)
            self.material_repo.remove(self.db, id=material_id)
        self.execute_in_transaction(_action)
