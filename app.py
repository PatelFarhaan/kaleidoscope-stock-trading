from project import app


#< !-- == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == -->
#                                 < !-- Admin Panel AngelFund -->
#< !-- == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == -->
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="127.0.0.1", port=5000)