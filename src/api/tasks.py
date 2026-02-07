from fastapi import Query, APIRouter, Body, HTTPException, status

from sqlalchemy import select, insert

from src.api.dependencies import PaginationDep
from src.database import async_session_marker
from src.models.tasks import TasksOrm
from src.schemas.tasks import TaskAdd

router = APIRouter(prefix='/router', tags=['Задачи'])

@router.get("", summary="Получение всех задач")
async def all_weeks_tasks(
        title: str | None = Query(None, description='Задача'),
        weekday: str | None = Query(None, description='День недели')
):
    async with async_session_marker() as session:
        query = select(TasksOrm)
        if weekday:
            query = query.where(TasksOrm.weekday.ilike(f'%{weekday}%'))
        if title:
            query = query.where(TasksOrm.title.ilike(f'%{title}%'))
        result = await session.execute(query)
        tasks = result.scalars().all()

        return tasks


@router.get("/{day}", summary="Получение задач за день")
async def one_weeks_tas(weekday: str):
    async with async_session_marker() as session:
        query = select(TasksOrm).where(TasksOrm.weekday.ilike(f'%{weekday}%'))
        result = await session.execute(query)
        tasks = result.scalar()


    return tasks if tasks else []

@router.post("/create_task", summary="Создание задачи")
async def create_task(task_data: TaskAdd = Body(openapi_examples={
            "normal": {
                "summary": "Пример создания задачи на понедельник",
                "value": {
                    "title": "Сделать отчёт",
                    "weekday": "monday"
                }
            },
            "вторник": {
                "summary": "Задача на вторник",
                "value": {
                    "title": "Встреча с командой",
                    "weekday": "tuesday"
                }
            }
        }
    )
):
    async with async_session_marker() as session:
        add_tasks = insert(TasksOrm).values(**task_data.model_dump())
        # print(add_hotels_stmt.compile(engine, compile_kwargs={"literal_binds": True})) - покажет сам запрос
        await session.execute(add_tasks)
        await session.commit()


    return {"status": "OK"}


@router.patch("/tasks/{task_id}/complete", summary="Отметить задачу выполненной")
async def mark_task_completed(task_id: int):
    async with async_session_marker() as session:
        # Находим задачу
        stmt = select(TasksOrm).where(TasksOrm.id == task_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(404, detail="Задача не найдена")

        # Меняем статус
        task.is_done = True
        await session.commit()

        return {"status": "OK", "message": f"Задача '{task.title}' отмечена выполненной"}
