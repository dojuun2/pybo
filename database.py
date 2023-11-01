from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 연결 URL(SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./pybo.db"

# 커넥션 풀 생성
# 커넥션 풀: 데이터베이스에 접속하는 객체를 일정 개수만큼 만들어놓고 돌려가며 사용하는 것을 말함
# 데이터 베이스에 접속하는 세션 수를 제어하고, 또 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# sessionmaker 클래스
# 데이터베이스와 상호작용하는 세션을 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base()
# 데이터베이스 모델을 정의하는 기본 베이스 클래스를 생성
# SQLAlchemy의 ORM을 사용하여 데이터베이스 테이블을 정의할 때 이 클래스를 상속
Base = declarative_base()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)


# db 세션 객체를 리턴하는 제너레이터 get_db 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        print(f"get_db() 오류 발생: {ex}")
    finally:
        db.close()