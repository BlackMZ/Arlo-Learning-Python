class User:
    def __init__(self, email, name, password, job_title):
        self.email = email
        self.name = name
        self.password = password
        self.job_title = job_title

    def change_password(self, new_password):
        self.password = new_password

    def change_job_title(self, new_job_title):
        self.job_title = new_job_title

    def get_user_info(self):
        print(f"User {self.name} job title is {self.job_title}")

if __name__ == '__main__':
    total_page = int((28 / 30)) + 1
    print(total_page)