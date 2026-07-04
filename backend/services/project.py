from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.project import ProjectCreate, ProjectUpdate, ProjectMemberCreate, ProjectPageResponse
from models.project import Project
from models.project_member import ProjectMember
from DAO import project as crud

logger = logging.getLogger(__name__)


async def create_project(project_info: ProjectCreate, db: AsyncSession, user_id: int):
    logger.info("创建项目请求: name=%s, owner_id=%s", project_info.name, user_id)

    existing = await crud.get_project_by_name(project_info.name, db)
    if existing:
        logger.warning("项目已存在: name=%s", project_info.name)
        raise HTTPException(
            status_code=400,
            detail="项目已经存在"
        )

    new_project = Project(
        name=project_info.name,
        description=project_info.description,
        owner_id=user_id
    )

    await crud.create_project(new_project, db)
    await db.flush()

    new_member = ProjectMember(
        project_id=new_project.id,
        user_id=user_id,
        role="PM"       # 默认这个项目属于 pm 负责
    )
    db.add(new_member)

    await db.commit()
    await db.refresh(new_project)

    logger.info("项目创建成功: id=%s", new_project.id)
    return new_project


async def get_project_list(page: int, page_size: int, user_id: int, db: AsyncSession):
    total, items = await crud.get_project_list_by_user(page, page_size, user_id, db)
    return ProjectPageResponse(
        total=total,
        items=items
    )


async def delete_project(project_id: int, db: AsyncSession):
    await crud.delete_project(project_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def update_project(project_id: int, update_data: ProjectUpdate, db: AsyncSession):
    logger.info("更新项目请求: project_id=%s", project_id)

    project = await crud.get_project_by_id(project_id, db)
    if not project:
        logger.warning("项目不存在: project_id=%s", project_id)
        raise HTTPException(
            status_code=404,
            detail="项目不存在"
        )

    # 更新时，项目的名称不能重复
    if update_data.name:
        existing = await crud.get_project_by_name(update_data.name, db)
        if existing and existing.id != project_id:
            # existing.id != project_id：确保同名项目 不是 当前正在编辑的项目，若没有这个判断->导致用户在不修改名称的情况下无法保存项目
            logger.warning("项目名称已存在: name=%s", update_data.name)
            raise HTTPException(
                status_code=400,
                detail="项目名已经存在"
            )

    update_dict = update_data.model_dump(exclude_unset=True)    # 模型对象->字典，exclude_unset=True 只包含前端传过来的字段

    update_dict["updated_at"] = datetime.now()  # 手动设置更新时间

    updated_project = await crud.update_project(project_id, update_dict, db)
    await db.commit()
    await db.refresh(updated_project)

    logger.info("项目更新成功: id=%s", updated_project.id)
    return updated_project


async def add_project_member(member_data: ProjectMemberCreate, db: AsyncSession):
    logger.info("添加项目成员: project_id=%s, user_id=%s", member_data.project_id, member_data.user_id)

    project = await crud.get_project_by_id(member_data.project_id, db)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="项目不存在"
        )

    new_member = ProjectMember(
        project_id=member_data.project_id,
        user_id=member_data.user_id,
        role=member_data.role
    )

    await crud.create_project_member(new_member, db)
    await db.commit()
    await db.refresh(new_member)

    return new_member


async def get_project_members(project_id: int, db: AsyncSession):
    members = await crud.get_project_members(project_id, db)
    return members


async def remove_project_member(member_id: int, db: AsyncSession):
    await crud.delete_project_member(member_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }
