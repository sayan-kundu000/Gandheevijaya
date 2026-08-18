from sqlalchemy.orm import Session

from backend.app.models.content import ExamCategory
from backend.app.repositories.base import BaseRepository
from backend.app.services.base import BaseService


class ExamCategoryRepository(BaseRepository[ExamCategory]):
    pass


def test_base_repository_crud(db_session: Session):
    repo = ExamCategoryRepository(ExamCategory)

    # 1. Create
    category = repo.create(db_session, obj_in={"name": "GATE Test", "slug": "gate-test"})
    assert category.id is not None
    assert category.name == "GATE Test"

    # 2. Count & Get
    count = repo.count(db_session)
    assert count >= 1

    fetched = repo.get(db_session, category.id)
    assert fetched is not None
    assert fetched.slug == "gate-test"

    # 3. Get multi
    items = repo.get_multi(db_session, skip=0, limit=10)
    assert len(items) >= 1

    # 4. Update
    updated = repo.update(db_session, db_obj=fetched, obj_in={"name": "GATE Computer Science"})
    assert updated.name == "GATE Computer Science"

    # 5. Remove
    removed = repo.remove(db_session, id=category.id)
    assert removed is not None
    assert repo.get(db_session, category.id) is None


def test_base_service_transaction(db_session: Session):
    service = BaseService(db_session)
    repo = ExamCategoryRepository(ExamCategory)

    def action():
        return repo.create(db_session, obj_in={"name": "ISRO CS", "slug": "isro-cs"})

    result = service.execute_in_transaction(action)
    assert result.id is not None
    assert result.slug == "isro-cs"
