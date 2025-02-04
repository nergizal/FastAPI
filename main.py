from fastapi import FastAPI,Body

app= FastAPI()

courses_db=[
    {'id':1,'instructor': 'Nergiz', 'tittle': 'Python', 'category': 'Development' },
    {'id':2,'instructor': 'Kemal', 'tittle': 'Flutter', 'category': 'Development' },
    {'id':3,'instructor': 'Atil', 'tittle': 'Kubernetes', 'category': 'Devops' },
]

@app.get("/courses")
async def get_all_courses():
    return courses_db



@app.get("/")
async def hello_world():
    return {"message": "Hello World"} #dictionary key value #JSON gösterimi için
#JSON- javascript object notation
#200 http kodu okey kod çalışıyor demektir.
#404 hata kodu
#500 kodda hata var demek
#422 sizin verdiğiniz şeyi işleyemiyorum.


#Path Paraameter

@app.get("/courses/{course_title}")#dinamik bir path parametresi
async def get_course(course_title:str): #bu fonksiyon asenkron çalışır, yani uzun süren işlemleri beklerken diğer işlemleri engellemez.
     for course in courses_db:
        if course.get('title').casefold() == course_title.casefold(): #casefold küçük büyük harf duyarlılığını kaldırarak karşılaştırma yapar.
            return course

#Bu fonksiyon çalıştırılmıyor.
@app.get("/courses/{course_id}")
async def get_course_by_id(course_id:str):
     for course in courses_db:
        if course.get('id').casefold() == course_id.casefold():
            return course

@app.get("/courses/byid/{course_id}")  #byid ekledik, url değişmiş gibi oldu.
async def get_course_by_id(course_id:int):
     for course in courses_db:
        if course.get('id') == course_id:
            return course


@app.get("/courses/")
async def get_category_by_query(category:str):
    courses_to_return=[]
    for course in courses_db:
        if course.get('category').casefold()== category.casefold():
            courses_to_return.append(course)
            return courses_to_return

@app.get("/courses/{course_instructor}/")
async def get_instructor_category_by_query(course_instructor: str, category:str):
    courses_to_return =[]
    for course in courses_db:
        if(course.get('instructor').casefold()== course_instructor.casefold()
            and course.get('category').casefold()== category.casefold()):
            courses_to_return.append(course)
            return course

@app.post("/courses/create_course")
async def create_course(new_course=Body()):
    courses_db.append(new_course)


@app.put("/courses/update_course")
async def update_courses(updated_course=Body()):
    for index in range(len(courses_db)):
        if courses_db[index].get("id")==updated_course.get("id"):
            courses_db[index]=updated_course

@app.delete("/courses/delete_course/{course_id}")
async def delete_course(course_id: int):
    for index in range(len(courses_db)):
        if courses_db[index].get("id")== course_id:
            courses_db.pop(index)
            break
