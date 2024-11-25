# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from database import get_db, Base

# # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board"


# engine = create_engine(
#     "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board-test"
# )

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture()
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()

#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
