# ANDRIES DANIEL LOUW | 25302262 | CTIP152 SS2

# GUI COLOURS
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

# IMPORTS
from data import librarians, failedAttempts, lockedAccounts, books


# A2: STAFF ID VALIDATION
def validateStaffID(staffID):
    if len(staffID) != 6:
        return False, "Staff ID must be 6 characters long"

    if "." not in staffID:
        return False, "Staff ID must include a period (.)"

    parts = staffID.split(".")

    if len(parts) != 2:
        return False, "Staff ID formate incorrect, example: js.123"

    letters, numbers = parts

    if len(letters) != 2 or not letters.isalpha():
        return False, "Staff ID must include 2 letters before the period (.)"

    if len(numbers) != 3 or not numbers.isdigit():
        return False, "Staff ID must include 3 numbers after the period (.)"

    return True, ""


# A2: PASSWORD VALIDATION
def validatePassword(password):
    if len(password) < 10:
        return False, "Password must be 10 or more characters long"

    if not any(char.isupper() for char in password):
        return False, "Password should include at least one uppercase letter"

    if not any(char.isdigit() for char in password):
        return False, "Password should include at least one number"

    if not any(char in "+-*/" for char in password):
        return False, "Password should include at least one operator (+, -, *, /)"

    return True, ""


# A2: FIRST AND LAST NAME VALIDATION
def validateName(name):
    if not name.isalpha():
        return False, "Name must only contain letters"

    return True, ""


# A2: REGISTER LIBRARIAN FUNCTION
def registerLibrarian(firstName, lastName, staffID, password):

    # FIRST NAME
    valid, message = validateName(firstName)
    if not valid:
        return False, "First Name must only contain letters"

    # LAST NAME
    valid, message = validateName(lastName)
    if not valid:
        return False, "Last Name must only contain letters"

    # STAFF ID
    valid, message = validateStaffID(staffID)
    if not valid:
        return False, message

    if staffID in librarians:
        return False, "Staff ID already exists"

    # PASSWORD
    valid, message = validatePassword(password)
    if not valid:
        return False, message

    # STORE IN LIBRARIANS

    librarians[staffID] = {
        "firstName": firstName,
        "lastName": lastName,
        "password": password,
    }

    return True, "LIBRARIAN SUCCESSFULLY REGISTERED"


# A2: LIBRARIAN AUTHENTICATION
def authenticateLibrarian(staffID, password):

    # CHECK IF ACCOUNT IS LOCKED
    if staffID in lockedAccounts:
        return False, "Account is locked"

    # CHECKS FOR STAFF ID
    if staffID not in librarians:
        return False, "Staff ID not found"

    # CHECK IF STAFF ID AND PASSWORD ARE CORRECT
    if librarians[staffID]["password"] == password:
        failedAttempts[staffID] = 0
        return True, "Login successful"

    # FAILED ATTEMPTS COUNTER
    failedAttempts[staffID] = failedAttempts.get(staffID, 0) + 1

    # LOCKING ACCOUNT AFTER 3 FAILED ATTEMPTS
    if failedAttempts[staffID] >= 3:
        lockedAccounts.add(staffID)
        return False, "Account has been locked"

    # INCORRECT PASSWORD
    return False, f"Incorrect password . Attempt {failedAttempts[staffID]} of 3"


# A1: MAIN MENU SECTION
def mainMenuSection():
    while True:

        # MENU SCREEN
        print(
            f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃      DIGITAL ARCHIVE PORTAL       ┃
          ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
          ┃     1 • REGISTER LIBRARIAN        ┃
          ┃     2 • STAFF LOG IN              ┃ 
          ┃     3 • SHUT DOWN SYSTEM          ┃ 
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
          {RESET}"""
        )

        try:
            option = int(
                input(
                    f"""{BOLD}{BLUE}                ➤ ENTER YOUR OPTION: {RESET}{BLUE}"""
                )
            )
        except ValueError:
            print(f"{RED}\n     • Invalid option. Please select between 1 | 2 | 3")
            continue

        # REGISTER LIBRARIAN
        if option == 1:
            registerSection()

        # STAFF LOG IN
        elif option == 2:
            loginSuccess = staffLogInSection()

            if loginSuccess:
                inventoryDashboard()

        # SHUT DOWN SYSTEM
        elif option == 3:
            print(
                f"""\n{BOLD}{RED}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃     SYSTEM SHUTTING DOWN...       ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
            )
            return False

        else:
            print(f"{RED}\n     • Invalid option. Please select between 1 | 2 | 3")


# A2: REGISTER SECTION
def registerSection():
    print(
        f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃         REGISTER LIBRARIAN        ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
    )

    # FIRST NAME VALIDATION
    while True:

        firstName = input(
            f"{BOLD}{BLUE}            ➤ ENTER FIRST NAME: {RESET}{BLUE}"
        ).strip()
        result, message = validateName(firstName)

        if result:
            print(f"{GREEN}               ✔︎")
            break
        else:
            print(f"{RESET}{RED}              • {message}")

    # Last NAME VALIDATION
    while True:

        lastName = input(
            f"{BOLD}{BLUE}\n            ➤ ENTER LAST NAME: {RESET}{BLUE}"
        ).strip()
        result, message = validateName(lastName)

        if result:
            print(f"{GREEN}               ✔︎")
            break
        else:
            print(f"{RESET}{RED}              • {message}")

    # STAFF ID VALIDATION
    while True:

        staffID = input(
            f"{BOLD}{BLUE}\n            ➤ CREATE STAFF ID: {RESET}{BLUE}"
        ).strip()
        result, message = validateStaffID(staffID)

        if result:
            print(f"{GREEN}               ✔︎")
            break

        if not result:
            print(f"{RESET}{RED}              • {message}")
            continue

        if staffID in librarians:
            print(f"{RED}              • Staff ID already exists")
            continue

        print(f"{GREEN}               ✔︎")
        break

    # PASSWORD VALIDATION
    while True:

        password = input(
            f"{BOLD}{BLUE}\n            ➤ CREATE PASSWORD: {RESET}{BLUE}"
        ).strip()
        result, message = validatePassword(password)

        if result:
            print(f"{GREEN}               ✔︎")
            break
        else:
            print(f"{RESET}{RED}              • {message}")

    result, message = registerLibrarian(firstName, lastName, staffID, password)
    print(
        f"""\n{BOLD}{GREEN}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃ {message} ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
    )


# A3: STAFF LOG IN SECTION
def staffLogInSection():
    print(
        f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃           STAFF LOG IN            ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
    )

    while True:
        # STAFF ID VALIDATION
        staffID = input(
            f"{BOLD}{BLUE}\n            ➤ ENTER STAFF ID: {RESET}{BLUE}"
        ).strip()
        result, message = validateStaffID(staffID)

        if not result:
            print(f"{RED}\n             • {message}")
            continue

        # PASSWORD VALIDATION
        password = input(
            f"{BOLD}{BLUE}\n            ➤ ENTER PASSWORD: {RESET}{BLUE}"
        ).strip()

        if password == "":
            print(f"{RESET}{RED}\n     • Password is required")
            continue

        # STAFF AUTHENTICATE
        result, message = authenticateLibrarian(staffID, password)

        if result:
            print(
                f"""\n{BOLD}{GREEN}
            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃       {message}       ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                """
            )
            return True
        else:
            print(f"{RESET}{RED}\n             • {message}")

            if "locked" in message.lower():
                return False


# B1: INVENTOTY DASHBOARD SECTION
def inventoryDashboard():

    # MENU
    while True:
        print(
            f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃        INVENTORY DASHBOARD        ┃
          ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
          ┃     1 • ADD BOOK                  ┃
          ┃     2 • GENERATE INVETORY REPORT  ┃ 
          ┃     3 • LOG OUT                   ┃ 
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
          {RESET}"""
        )

        try:
            option = int(
                input(
                    f"""{BOLD}{BLUE}                ➤ ENTER YOUR OPTION: {RESET}{BLUE}"""
                )
            )
        except ValueError:
            print(f"{RED}\n     • Invalid option. Please select between 1 | 2 | 3")
            continue

        # ADD BOOKS
        if option == 1:
            addBookSection()

        # GENERATE REPORT
        elif option == 2:
            print(f"{RED}\n     • INVENTORY REPORT FEATURE - Comming Soon")

        # LOG OUT
        elif option == 3:
            print(
                f"""\n{BOLD}{RED}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃           LOGGING OUT...          ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
            )
            break

        else:
            print(f"{RED}\n     • Invalid option. Please select between 1 | 2 | 3")


# B2: BOOK TITLE VALIDATION
def validateBookTitle(title):

    if title == "":
        return False, "Book title can not be empty"

    if len(title) > 30:
        return False, "Book title can not be longer than 30 characters"

    return True, ""


# B2: ISBN VALIDATION
def validateISBN(isbn):

    if len(isbn) != 13:
        return False, "ISBN must be 13 numbers exactly"

    if not isbn.isdigit():
        return False, "ISBN must only include numbers"

    return True, ""


# B3: AUTO GENERATED ACCESSION NUMBER
def generateAccessionNumber(title, index):
    firstletters = title[:3].upper()
    return f"BK-{firstletters}-{index:02d}"


# B2: ADD BOOK SECTION
def addBookSection():
    print(
        f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃             ADD BOOKS             ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
    )

    # NUMBER OF BOOKS
    while True:
        try:
            numberOfBooks = int(
                input(
                    f"""{BOLD}{BLUE}         ➤ ENTER NUMBER OF BOOKS TO CATELOGUE: {RESET}{BLUE}"""
                )
            )

            if numberOfBooks <= 0:
                print(
                    f"{RED}\n     • Invalid option. Please select enter a number bigger than 0"
                )
                continue
            break

        except ValueError:
            print(f"{RED}\n     • Invalid option. Please enter a number")

        # ADD BOOK
    for index in range(1, numberOfBooks + 1):
        print(
            f"""\n{BOLD}{BLUE}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃          + ADD BOOK            ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
        )

        # TITLE VALIDATION
        while True:
            title = input(
                f"{BOLD}{BLUE}            ➤ ENTER BOOK TITLE: {RESET}{BLUE}"
            ).strip()
            result, message = validateBookTitle(title)

            if result:
                print(f"{GREEN}               ✔︎")
                break

            print(f"{RESET}{RED}              • {message}")

        # ISBN VALIDATION
        while True:
            isbn = input(
                f"{BOLD}{BLUE}            ➤ ENTER ISBN NUMBER: {RESET}{BLUE}"
            ).strip()
            result, message = validateISBN(isbn)

            if result:
                print(f"{GREEN}               ✔︎")
                break

            print(f"{RESET}{RED}              • {message}")

        accessionNumber = generateAccessionNumber(title, index)

        # ADD TO BOOKS ARRAY
        books.append({"accessionNumber": accessionNumber, "title": title, "isbn": isbn})

        print(
            f"""\n{BOLD}{GREEN}
          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ┃       ✔︎ BOOK ADDED        ┃
          ┃         {accessionNumber}         ┃
          ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            """
        )
