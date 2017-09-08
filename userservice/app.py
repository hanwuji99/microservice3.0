from services.user import  app as userapp


if __name__ == "__main__":
    userapp.run(host="0.0.0.0", port=5000, debug=True)


