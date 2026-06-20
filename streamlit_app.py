import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LegalConnect",
    page_icon="⚖️",
    layout="wide"
)



if "token" not in st.session_state:
    st.session_state.token = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }




st.title("⚖️ LegalConnect")
st.caption("Lawyer & Client Case Management System")


menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Register",
        "Login",
        "Profile",
        "Create Complaint",
        "My Complaints",
        "Cases",
        "Logout"
    ]
)



if menu == "Register":

    st.header("Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        ["client", "lawyer"]
    )

    if st.button("Register"):

        payload = {
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }

        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=payload
        )

        if response.status_code in [200, 201]:
            st.success("Registration Successful")
        else:
            st.error(response.text)



elif menu == "Login":

    st.header("Login")

    username = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state.token = token
            st.session_state.logged_in = True

            st.success("Login Successful")

        else:
            st.error(response.text)



elif menu == "Profile":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("My Profile")

    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=get_headers()
    )

    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(response.text)


elif menu == "Create Complaint":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("File Complaint")

    title = st.text_input("Title")

    description = st.text_area(
        "Description"
    )

    category = st.selectbox(
        "Category",
        [
            "Civil",
            "Criminal",
            "Consumer",
            "Property",
            "Family",
            "Corporate"
        ]
    )

    urgency = st.selectbox(
        "Urgency",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    preferred_lawyer_id = st.number_input(
        "Preferred Lawyer ID",
        min_value=0,
        value=0
    )

    if st.button("Submit Complaint"):

        payload = {
            "title": title,
            "description": description,
            "category": category,
            "urgency": urgency,
            "preferred_lawyer_id": preferred_lawyer_id
        }

        response = requests.post(
            f"{BASE_URL}/complaints/",
            json=payload,
            headers=get_headers()
        )

        if response.status_code in [200, 201]:
            st.success("Complaint Submitted")
            st.json(response.json())
        else:
            st.error(response.text)



elif menu == "My Complaints":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("My Complaints")

    response = requests.get(
        f"{BASE_URL}/complaints/",
        headers=get_headers()
    )

    if response.status_code == 200:

        complaints = response.json()

        if complaints:
            st.dataframe(
                pd.DataFrame(complaints),
                use_container_width=True
            )
        else:
            st.info("No complaints found")

    else:
        st.error(response.text)


elif menu == "Cases":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.stop()

    st.header("Case Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "View Cases",
            "Create Case",
            "Update Status",
            "Update Hearing",
            "Update Notes"
        ]
    )

 

    with tab1:

        response = requests.get(
            f"{BASE_URL}/cases/",
            headers=get_headers()
        )

        if response.status_code == 200:

            cases = response.json()

            if cases:
                st.dataframe(
                    pd.DataFrame(cases),
                    use_container_width=True
                )
            else:
                st.info("No cases found")

        else:
            st.error(response.text)



    with tab2:

        complaint_id = st.number_input(
            "Complaint ID",
            min_value=1
        )

        lawyer_id = st.number_input(
            "Lawyer ID",
            min_value=1
        )

        hearing_date = st.date_input(
            "Hearing Date"
        )

        if st.button("Create Case"):

            payload = {
                "complaint_id": complaint_id,
                "lawyer_id": lawyer_id,
                "hearing_date": hearing_date.isoformat()
            }

            response = requests.post(
                f"{BASE_URL}/cases/",
                json=payload,
                headers=get_headers()
            )

            if response.status_code in [200, 201]:
                st.success("Case Created")
                st.json(response.json())
            else:
                st.error(response.text)



    with tab3:

        case_id = st.number_input(
            "Case ID",
            min_value=1,
            key="status_case"
        )

        status = st.text_input(
            "New Status"
        )

        if st.button("Update Status"):

            response = requests.put(
                f"{BASE_URL}/cases/{case_id}/status",
                params={
                    "status_text": status
                },
                headers=get_headers()
            )

            st.write(response.text)



    with tab4:

        case_id = st.number_input(
            "Case ID",
            min_value=1,
            key="hearing_case"
        )

        hearing_date = st.date_input(
            "New Hearing Date",
            key="hearing_date"
        )

        if st.button("Update Hearing Date"):

            response = requests.put(
                f"{BASE_URL}/cases/{case_id}/hearing",
                params={
                    "hearing_date": hearing_date.isoformat()
                },
                headers=get_headers()
            )

            st.write(response.text)



    with tab5:

        case_id = st.number_input(
            "Case ID",
            min_value=1,
            key="notes_case"
        )

        notes = st.text_area(
            "Notes"
        )

        if st.button("Update Notes"):

            response = requests.put(
                f"{BASE_URL}/cases/{case_id}/notes",
                params={
                    "notes": notes
                },
                headers=get_headers()
            )

            st.write(response.text)


elif menu == "Logout":

    st.session_state.token = None
    st.session_state.logged_in = False

    st.success("Logged Out")