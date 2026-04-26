from pymongo import MongoClient

def seed_database():
    print("Connecting to MongoDB...")
    # Change URI if you moved to Atlas, otherwise leave as localhost
    client = MongoClient("mongodb://localhost:27017/")
    db = client['internship_matching_db']

    # Clear old data so we start fresh
    db.students.drop()
    db.employers.drop()

    print("Generating 10 High-Fidelity Student Profiles...")
    students_data = [
        {
            "name": "Aarav Patel", "email": "aarav@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Mumbai, MH",
            "skills": "Python, Embedded C, Arduino, Raspberry Pi, MATLAB", 
            "interests": "IoT, Robotics, Automation, Smart Devices", 
            "aspirations": "I want to build hardware systems that integrate with cloud AI.", 
            "academic_background": "B.E. Electronics and Telecommunication Engineering, Shah & Anchor Kutchhi Engineering College"
        },
        {
            "name": "Priya Sharma", "email": "priya@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Pune, MH",
            "skills": "React.js, HTML5, CSS3, Tailwind, Figma", 
            "interests": "User Interface Design, Frontend Architecture, Accessibility", 
            "aspirations": "Aiming to become a Lead Frontend Engineer crafting beautiful web apps.", 
            "academic_background": "B.S. Computer Science"
        },
        {
            "name": "Rohan Gupta", "email": "rohan@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Bangalore, KA",
            "skills": "Python, TensorFlow, PyTorch, Pandas, SQL", 
            "interests": "Machine Learning, Deep Learning, Natural Language Processing", 
            "aspirations": "Looking to train LLMs and work on generative AI technologies.", 
            "academic_background": "M.S. Data Science and Artificial Intelligence"
        },
        {
            "name": "Neha Desai", "email": "neha@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Mumbai, MH",
            "skills": "Node.js, Express, MongoDB, Docker, AWS", 
            "interests": "Backend Development, Microservices, Cloud Security", 
            "aspirations": "To become a Cloud Solutions Architect for high-traffic platforms.", 
            "academic_background": "B.E. Information Technology"
        },
        {
            "name": "Karan Singh", "email": "karan@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Delhi, DL",
            "skills": "Excel, PowerPoint, Market Research, Communication", 
            "interests": "Machine Learning, Artificial Intelligence, Tech Startups", 
            "aspirations": "I want to manage AI projects and lead tech teams.", 
            "academic_background": "B.B.A. Business Administration"
        },
        {
            "name": "Vikram Verma", "email": "vikram@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Hyderabad, TS",
            "skills": "Linux, Wireshark, Bash Scripting, Network Routing, Cryptography", 
            "interests": "Cybersecurity, Ethical Hacking, Penetration Testing", 
            "aspirations": "I want to protect corporate networks from advanced cyber threats.", 
            "academic_background": "B.E. Computer Engineering"
        },
        {
            "name": "Anjali Iyer", "email": "anjali@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Chennai, TN",
            "skills": "Flutter, Dart, Firebase, Swift, Android Studio", 
            "interests": "Mobile App Development, Cross-Platform Architecture", 
            "aspirations": "To build mobile applications that reach millions of users globally.", 
            "academic_background": "B.Tech Software Engineering"
        },
        {
            "name": "Rahul Bose", "email": "rahul@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Kolkata, WB",
            "skills": "SQL, Advanced Excel, PowerBI, Tableau, Data Cleaning", 
            "interests": "Artificial Intelligence, Predictive Analytics, Machine Learning", 
            "aspirations": "I want to be a Machine Learning Engineer handling big data.", 
            "academic_background": "B.S. Statistics"
        },
        {
            "name": "Sneha Reddy", "email": "sneha@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Ahmedabad, GJ",
            "skills": "Figma, Adobe XD, Illustrator, Wireframing, User Research", 
            "interests": "Web Development, Frontend Coding, User Experience", 
            "aspirations": "To design intuitive interfaces that bridge the gap between users and complex systems.", 
            "academic_background": "B.Des Visual Communication"
        },
        {
            "name": "Aditya Joshi", "email": "aditya@test.com", "password": "123456789", "phone": "0123456789",
            "location": "Pune, MH",
            "skills": "Docker, Kubernetes, Jenkins, Git, Linux Administration", 
            "interests": "Cloud Computing, CI/CD Pipelines, System Reliability", 
            "aspirations": "I want to become a DevOps Engineer ensuring 99.9% server uptime.", 
            "academic_background": "B.E. Information Technology"
        }
    ]
    db.students.insert_many(students_data)

    print("Generating 10 High-Fidelity Employer Profiles...")
    employers_data = [
        {
            "company_name": "TechForge Hardware", "email": "hr@techforge.com", "password": "123456789", 
            "position_offered": "Embedded Systems Intern", 
            "description": "Join our R&D team to design next-generation smart home devices. We need someone passionate about hardware-software integration.", 
            "required_skills": "Embedded C, Microcontrollers, Arduino, Python", 
            "location_of_work": "Navi Mumbai, MH", "stipend": "₹15,000/month"
        },
        {
            "company_name": "NeuroNet Labs", "email": "hiring@neuronet.ai", "password": "123456789", 
            "position_offered": "AI Research Intern", 
            "description": "We are a fast-paced startup building custom NLP models. Must be comfortable reading research papers and translating them into code.", 
            "required_skills": "Python, TensorFlow, PyTorch, Scikit-Learn", 
            "location_of_work": "Remote", "stipend": "₹25,000/month"
        },
        {
            "company_name": "CloudScale Solutions", "email": "jobs@cloudscale.in", "password": "123456789", 
            "position_offered": "Backend Cloud Intern", 
            "description": "Help us scale our APIs from thousands to millions of requests. We value clean code and scalable architecture.", 
            "required_skills": "Node.js, Express, MongoDB, REST APIs", 
            "location_of_work": "Pune, MH", "stipend": "₹20,000/month"
        },
        {
            "company_name": "PixelPerfect Agency", "email": "careers@pixelperfect.com", "password": "123456789", 
            "position_offered": "Frontend Web Developer", 
            "description": "We create stunning websites for global brands. If you have an eye for design and the coding chops to bring UI to life, we want you.", 
            "required_skills": "React.js, JavaScript, HTML, CSS", 
            "location_of_work": "Bangalore, KA", "stipend": "₹18,000/month"
        },
        {
            "company_name": "Visionary AI Startups", "email": "founder@visionary.ai", "password": "123456789", 
            "position_offered": "Tech Product Management Intern", 
            "description": "We need help organizing sprints and planning our AI product roadmap. No coding required, but you must understand the tech landscape.", 
            "required_skills": "Market Research, Communication, Agile/Scrum, Excel", 
            "location_of_work": "Delhi, DL (Hybrid)", "stipend": "₹12,000/month"
        },
        {
            "company_name": "SecureTech Vault", "email": "hr@securetech.com", "password": "123456789", 
            "position_offered": "Cybersecurity Analyst Intern", 
            "description": "Monitor network traffic and assist in vulnerability assessments. You will be actively looking for exploits in our client environments.", 
            "required_skills": "Networking, Wireshark, Linux, Ethical Hacking", 
            "location_of_work": "Hyderabad, TS", "stipend": "₹16,000/month"
        },
        {
            "company_name": "AppMakers Inc", "email": "jobs@appmakers.com", "password": "123456789", 
            "position_offered": "Mobile App Developer", 
            "description": "Help us build out cross-platform features for our flagship application. You will work directly with our lead mobile architect.", 
            "required_skills": "Flutter, Dart, Firebase, Mobile UI", 
            "location_of_work": "Chennai, TN", "stipend": "₹18,000/month"
        },
        {
            "company_name": "DataPoint Insights", "email": "careers@datapoint.in", "password": "123456789", 
            "position_offered": "Data Analytics Intern", 
            "description": "Transform raw company data into readable dashboards for our executive team. Strong visualization skills are an absolute must.", 
            "required_skills": "SQL, Tableau, Excel, PowerBI", 
            "location_of_work": "Kolkata, WB", "stipend": "₹14,000/month"
        },
        {
            "company_name": "Creative Canvas Studios", "email": "design@creativecanvas.com", "password": "123456789", 
            "position_offered": "UX/UI Design Intern", 
            "description": "We need a creative mind to build wireframes and user flows. You won't be coding, but you'll be designing what the coders build.", 
            "required_skills": "Figma, User Research, Wireframing, Prototyping", 
            "location_of_work": "Ahmedabad, GJ", "stipend": "₹15,000/month"
        },
        {
            "company_name": "InfraCloud Networks", "email": "cloud@infracloud.com", "password": "123456789", 
            "position_offered": "DevOps Engineering Intern", 
            "description": "Assist our infrastructure team with containerizing applications and maintaining deployment pipelines. Linux experience is required.", 
            "required_skills": "Docker, Kubernetes, Linux, AWS, CI/CD", 
            "location_of_work": "Pune, MH", "stipend": "₹22,000/month"
        }
    ]
    db.employers.insert_many(employers_data)

    print("Success! 20 deeply engineered test profiles injected.")

if __name__ == "__main__":
    seed_database()