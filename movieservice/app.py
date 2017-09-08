from services.movies import  app as movieapp


if __name__ == "__main__":
    movieapp.run(host='0.0.0.0', port=5001, debug=True)


