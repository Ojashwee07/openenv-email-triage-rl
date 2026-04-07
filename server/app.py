from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Space is running"}

def main():
    print("Server started")

if __name__ == "__main__":
    main()
