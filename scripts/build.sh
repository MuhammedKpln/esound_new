pyinstaller src/main.py --onefile --hidden-import "dependency_injector.
errors" --hidden-import "six" --add-data="src/database/base.sql:src/database/base.sql"