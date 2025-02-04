from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Course:
    id: int
    title: str
    instructor: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, instructor: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.rating = rating
        self.published_date = published_date


class CourseRequest(BaseModel):
    id: Optional[int] = Field(description="The id of course.optional", default=None)
    title: str = Field(min_length=3,
                       max_length=100)  #istek gelmeden bunlarda hata varsa kullanıcıya göstermeye olanak tanıyabilir.
    instructor: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gte=2020, lte=2100)  #gte:greater tha or equal
    #bi değeri override ediyorsun,kullanmak opsiyonel
    model_config = {
        "json_schema_extra":{
            "example": {
            "title": "My Course",
            "instructor": "nergiz",
            "rating":5

            }
        }
    }


courses_db = [
    Course(1, "Python", "nergiz", 5, 2025),
    Course(2, "Kotlin", "ahmet", 5, 2029),
    Course(3, "Jenkins", "nergiz", 5, 2023),
    Course(4, "Kubernetes", "atıl", 2, 2030),
    Course(5, "Machine Learning", "zeynep", 3, 2036),
    Course(6, "Deep learning", "ayşe", 1, 2039)]


@app.get("/courses", status_code=status.HTTP_200_OK)
async def get_all_courses():
    return courses_db


@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: int = Path(gt=0)):  # gt= greater than demek
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating: int = Query(gt=0, lt=6)):  #valide etmiş oluyoruz
    courses_to_return = []
    for course in courses_db:
        if course.rating == course_rating:
            courses_to_return.append(course)
    return courses_to_return


@app.get("/courses/publish/", status_code=status.HTTP_200_OK)  #statik bir path, adresi değiştirmedik.
async def get_courses_by_publish_date(publish_date: int = Query(gt=2005, lt=2040)):
    courses_to_return = []
    for course in courses_db:
        if course.published_date == publish_date:
            courses_to_return.append(course)
            return courses_to_return


@app.post("/create_course", status_code=status.HTTP_201_CREATED)
async def create_course(course_request: CourseRequest): #Body'i kendimiz oluşturacağız.
    new_course= Course(**course_request.model_dump()) #kısa yol tek tek de yazılabilir
    courses_db.append(find_course_id(new_course))

def find_course_id(course: Course):
    course.id=1 if  len(courses_db)==0 else courses_db[-1].id+ 1 # -1 son elemanı veriyor.
    return course


@app.put ("/courses/update_courses", status_code=status.HTTP_204_NO_CONTENT)
async def update_course(course_request: CourseRequest):
    course_updated =False
    for i in range(len(courses_db)):
        if courses_db[i].id== course_request.id:
            courses_db[i]=course_request
            course_updated= True
    if not course_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/courses/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int =Path(gt=0)):
    course_deleted=False
    for i in range(len(courses_db)):
        if courses_db[i].id ==course_id:
            courses_db.pop(i)
            courses_deleted =True
            break
        if not course_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cours enot found")