from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app
from app.models.base import db


app = create_app()
manager = Manager(app, db)

migrate = Migrate(app, db)
# 模型 -> 迁移文件 -> 表
# 1.要使用flask_migrate,必须绑定app和DB
# migrate.init_app(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
