import sys
import os

# เพิ่ม backend เข้าไปใน sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from Backend.app import app  # import app จาก backend

if __name__ == "__main__":
    app.run()
