## Steps to setup backend
1. Shift to the backend directory: `cd backend`
2. Setup python virtual environment with `python3 -m venv .venv`
3. Activate environment: `source .venv/bin/activate`
4. Install requirements: `pip3 install -r requirements.txt`
5. Add your credentials in `.env` file
6. Run the application with: `uvicorn main:app --reload`
