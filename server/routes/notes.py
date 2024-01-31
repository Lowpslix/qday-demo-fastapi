from typing import Optional, Dict, Annotated
from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from server.models.notes import Note, UpdateNote, Category


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_description="List all notes", response_class=HTMLResponse)
async def home(request: Request) -> list[Note]:
    notes = await Note.find_all().to_list()
    categories = await Category.find_all().to_list()

    notes_for_template = [
        {"id": str(note.id), "content": note.content} for note in notes
    ]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "notes": notes_for_template, "categories": categories},
    )


@router.post("/add-category", response_description="Add new category")
async def create_category(category: Category) -> Category:
    await category.insert()
    return category


@router.post(
    "/add-note", response_description="Add new note", response_class=RedirectResponse
)
async def create_note(
    content: Annotated[str, Form(...)], category: Annotated[str, Form(...)]
) -> Note:
    find_category = await Category.find_one(Category.name == category)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    new_note = Note(content=content, category=find_category)
    await new_note.insert()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.post(
    "/complete/{id}",
    response_description="Complete note",
    response_class=RedirectResponse,
)
async def delete_note(id: PydanticObjectId) -> Note:
    note = await Note.get(id)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note {id} not found"
        )

    await note.delete()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.post(
    "/update/{id}", response_description="Update note", response_class=RedirectResponse
)
async def update_note(
    updated_content: Annotated[str, Form(...)],
    id: PydanticObjectId,
) -> Note:
    note = await Note.get(id)

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note {id} not found"
        )

    await note.set({Note.content: updated_content})
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
