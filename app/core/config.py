import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") 
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
URL = os.getenv("url")


SUBJECTS = {
  "BE": {
    "CSE": {
      "1": [
        "Calculus",
        "Physics",
        "Professional Communication",
        "Workshop/Fundamentals of Biotechnology",
        "Programming Fundamentals",
        "Universal Human Values"
      ],
      "2": [
        "Basic Electrical and Electronics Engineering",
        "Applied Chemistry",
        "Engineering Graphics",
        "Object Oriented Programming",
        "Differential Equations and Transforms",
        "Environmental Sciences"
      ],
      "3": [
        "Data Structures",
        "Database Systems",
        "Discrete Structures",
        "Web Technologies",
        "Software Engineering",
        "Latest Trends and Technologies in Computer Science"
      ],
      "4": [
        "Analysis and Design of Algorithms",
        "Linear Algebra and Probability Theory",
        "Operating Systems",
        "Computer Networks",
        "Computer Architecture and Organization"
      ],
      "5": [
        "Natural Language Processing",
        "Computer Graphics",
        "Artificial Intelligence",
        "Theory of Computation",
        "Economics",
        "Industrial Training"
      ],
      "6": [
        "Data Mining and Machine Learning",
        "Cryptography and Network Security",
        "Digital Image Processing",
        "Compiler Design",
        "Elective-I"
      ],
      "7": [
        "Neural Networks and Deep Learning",
        "Cyber Laws and IPR",
        "Elective-II",
        "Elective-III",
        "Project-I",
        "Industrial Training"
      ],
      "8": [
        "Project-II (Expected)",
        "Seminar (Expected)",
        "Comprehensive Viva (Expected)",
        "Elective-IV (Expected)",
        "Elective-V (Expected)"
      ]
    },

    "IT": {
      "1": [
        "Calculus",
        "Physics",
        "Professional Communication",
        "Workshop / Fundamentals of Biotechnology",
        "Programming Fundamentals",
        "Universal Human Values"
      ],
      "2": [
        "Applied Chemistry",
        "Differential Equations and Transforms",
        "Basic Electrical and Electronics Engineering",
        "Engineering Graphics",
        "Object Oriented Programming using C++",
        "Environment Sciences"
      ],
      "3": [
        "Linear Algebra and Probability Theory",
        "Data Structures",
        "Data Structures(P)",
        "Digital Electronics",
        "Digital Electronics(P)",
        "Computer Architecture and Organization",
        "Database Management System",
        "Database Management System(P)"
      ],
      "4": [
        "Elective-I (Humanities and Social Sciences)",
        "Discrete Structures",
        "Microprocessor & Assembly Language Programming",
        "Microprocessor & Assembly Language Programming(P)",
        "Computer Networks",
        "Computer Networks(P)",
        "Operating System",
        "Operating System(P)"
      ],
      "5": [
        "Network Security and Cryptography",
        "Network Security and Cryptography(P)",
        "Artificial Intelligence",
        "Artificial Intelligence(P)",
        "Professional Elective-I",
        "Professional Elective-I(P)",
        "Industrial Training (after 4th semester)",
        "Cyber Laws & IPR"
      ],
      "6": [
        "Theory of Computation",
        "Machine Learning",
        "Machine Learning(P)",
        "Design and Analysis of Algorithms",
        "Design and Analysis of Algorithms(P)",
        "Professional Elective-II",
        "Professional Elective-III",
        "Open Elective-I"
      ],
      "7": [
        "Digital Signal Processing",
        "Digital Signal Processing(P)",
        "Compiler Design",
        "Professional Elective-IV",
        "Management Elective (Choice Based)",
        "Industrial Training (after 6th Semester)"
      ],
      "8": [
        "Embedded System Design",
        "Embedded System Design(P)",
        "Cloud Computing",
        "Professional Elective-V",
        "Project IV",
        "Seminar",
        "Industrial Training"
      ]
    },

    "ECE": {
      "1": [
        "Basic Electrical and Electronics Engineering",
        "Engineering Graphics",
        "Applied Chemistry",
        "Calculus",
        "Programming Fundamentals"
      ],
      "2": [
        "Workshop",
        "Digital Design",
        "Professional Communication",
        "UHV",
        "Applies Physics"
      ],
      "3": [
        "Linear Algebra and Complex Analysis",
        "Signals and Systems",
        "Microprocessor and Microcontroller",
        "Electronic Devices and Circuits",
        "Electronics Measurementsand Instrumentation",
        "Economics"
      ],
      "4": [
        "Communication Engineering",
        "Advance Microcontroller and Application",
        "Analog Electronics Circuits",
        "Probability and Random Process",
        "Electromagnetic Theory",
        "Network Analysis"
      ],
      "5": ["VLSI", "AWP", "DSD", "DSA", "DSP", "CN"],
      "6": [
        "Microwave & Radar Engineering",
        "Fibre Optic Communication Systems",
        "Digital Communication",
        "Control Systems",
        "Power Electronics",
        "Satellite Communication"
      ],
      "7": [
        "Wireless and Mobile Communication",
        "Embedded System Design"
      ],
      "8": [""]
    },

    "MECH": {
      "1": [
        "Applied Chemistry",
        "Applied Chemistry (P)",
        "Calculus",
        "Professional Communication",
        "Professional Communication (P)",
        "Workshop / Fundamentals of Biotechnology",
        "Engineering Mechanics",
        "Engineering Mechanics (P)",
        "Environment Sciences"
      ],
      "2": [
        "Physics",
        "Physics (P)",
        "Differential Equations and Transforms",
        "Basics of Electrical and Electronics Engineering",
        "Basics of Electrical and Electronics Engineering (P)",
        "Engineering Graphics",
        "Engineering Graphics (P)",
        "Programming Fundamentals",
        "Programming Fundamentals (P)",
        "Universal Human Values",
        "Product Re-engineering and Innovation"
      ],
      "3": [
        "Basic Thermodynamics",
        "Basic Thermodynamics (P)",
        "Mechanics of Materials",
        "Mechanics of Materials (P)",
        "Kinematics of Machines",
        "Kinematics of Machines (P)",
        "Machine Drawing",
        "Machine Drawing (P)",
        "Manufacturing Processes",
        "Manufacturing Processes (P)",
        "Algebra and Complex Analysis"
      ],
      "4": [
        "Engineering Thermodynamics",
        "Engineering Thermodynamics (P)",
        "Mechanics of Solids",
        "Mechanics of Solids (P)",
        "Dynamics of Machines",
        "Dynamics of Machines (P)",
        "Manufacturing Technology",
        "Manufacturing Technology (P)",
        "Fluid Mechanics",
        "Fluid Mechanics (P)",
        "Numerical Analysis",
        "Numerical Analysis (P)"
      ],
      "5": [
        "Design of Machine Elements",
        "Design of Machine Elements 1 (P)",
        "Computer Aided Design and Manufacturing",
        "Computer Aided Design and Manufacturing (P)",
        "Robotics",
        "Robotics (P)",
        "Mechanical Measurement",
        "Mechanical Measurement (P)",
        "Mechatronics",
        "Mechatronics(P)",
        "Fluid Machinery",
        "Fluid Machinery (P)"
      ],
      "6": [
        "Design of Machine Elements 2",
        "Design of Machine Elements 2 (P)",
        "Finite Element Methods",
        "Finite Element Methods (P)",
        "Mechanical Vibrations",
        "Mechanical Vibrations (P)",
        "Heat Transfer",
        "Heat Transfer (P)",
        "Mechanical Behaviour of Materials",
        "Mechanical Behaviour of Materials (P)",
        "Advanced Manufacturing Techniques",
        "Advanced Manufacturing Techniques (P)"
      ],
      "7": [
        "Refrigeration and Air Conditioning",
        "Refrigeration and Air Conditioning (P)",
        "Automatic Control",
        "Automatic Control (P)",
        "Vehicle Dynamics",
        "Vehicle Dynamics (P)",
        "Elective 1",
        "Elective 2"
      ],
      "8": [
        "Operations Research",
        "Operations Research (P)",
        "Non-conventional energy sources",
        "Computational Fluid Dynamics",
        "Computational Fluid Dynamics (P)",
        "Elective 3",
        "Elective 4",
        "Major Project"
      ]
    },

    "EEE": {
      "1": [
        "Applied Chemistry",
        "Applied Chemistry (P)",
        "Calculus",
        "Basic Electrical and Electronics Engineering",
        "Basic Electrical and Electronics Engineering (P)",
        "Engineering Graphics",
        "Engineering Graphics (P)",
        "Programming Fundamentals",
        "Programming Fundamentals (P)",
        "Environment Sciences"
      ],
      "2": [
        "Physics",
        "Physics (P)",
        "Differential Equations and Transforms",
        "Professional Communication",
        "Professional Communication (P)",
        "Workshop / Fundamentals of Biotechnology",
        "Fundamentals of Electrical Engineering",
        "Fundamentals of Electrical Engineering (P)",
        "Universal Human Values"
      ],
      "3": [
        "Networks Analysis and Synthesis",
        "Networks Analysis and Synthesis Lab",
        "Electrical Machine-I",
        "Electrical Machine-I Lab",
        "Analog Electronics",
        "Analog Electronics Lab",
        "Digital Electronics",
        "Digital Electronics Lab",
        "Maths-III",
        "MATLAB"
      ],
      "4": [
        "Electrical Machine-II",
        "Electrical Machine-II Lab",
        "Power System-I",
        "Power System-I Lab",
        "Control Engineering-I",
        "Control Engineering-I Lab",
        "Microprocessor & Microcontroller",
        "Microprocessor & Microcontroller Lab",
        "Economics"
      ],
      "5": [
        "Power System-II",
        "Power System-II Lab",
        "Control Engineering-II",
        "Control Engineering-II Lab",
        "Electromagnetic Field Theory",
        "Professional Elective-I",
        "Professional Elective-I Lab",
        "Computer Networks",
        "Vocational Training"
      ],
      "6": [
        "CAPSA",
        "CAPSA Lab",
        "Power Electronics",
        "Power Electronics Lab",
        "Professional Elective-II",
        "Professional Elective-II Lab",
        "Signal and Systems",
        "Professional Elective-III"
      ],
      "7": [
        "Power Electronics & Drives",
        "Power Electronics & Drives Lab",
        "Professional Elective-IV",
        "Professional Elective-V",
        "Professional Elective-V Lab",
        "Open Elective-I",
        "Project-I",
        "Vocational Training"
      ],
      "8": [
        "Professional Elective",
        "Open elective-II",
        "Open elective-II Lab",
        "Open Elective -III",
        "Cyber Laws and IPR",
        "Project-II"
      ]
    },

    "BIOTECH": {
      "1": [
        "Calculus",
        "Physics",
        "Professional Communication",
        "Workshop / Fundamentals of Biotechnology",
        "Basic Electrical and Electronics Engineering",
        "Universal Human Values"
      ],
      "2": [
        "Applied Chemistry",
        "Differential Equations and Transforms",
        "Programming Fundamentals",
        "Engineering Graphics",
        "Fundamentals of Bioengineering",
        "Environment Sciences"
      ],
      "3": [
        "Process Calculations",
        "Microbiology",
        "Biochemistry",
        "Cell Biology & Genetics",
        "Elective I (Economics / Psychology / Sociology)"
      ],
      "4": [
        "Molecular Biology",
        "Thermodynamics",
        "Chemical Reaction Engineering",
        "Industrial Biotechnology",
        "Immunology & Immunotechnology"
      ],
      "5": [
        "Enzyme Engineering & Technology",
        "Bio-Process Engineering",
        "Animal Cell Culture & Biotechnology",
        "Transport Phenomena",
        "Bioinstrumentation",
        "Training (After 4th Sem)"
      ],
      "6": [
        "Recombinant DNA Technology",
        "Bio-Informatics",
        "Bioreactor Design and Operation",
        "Down Stream Processing",
        "Open Elective (Biomaterials)"
      ],
      "7": [
        "Environmental Biotechnology",
        "Food Biotechnology",
        "Plant Tissue Culture",
        "Bio-analytical Techniques",
        "Minor Project",
        "Training (After 6th Sem)"
      ],
      "8": [
        "Major Project",
        "Enzyme Catalyzed Organic Synthesis",
        "Project Management and Entrepreneurship",
        "Modeling and Simulation of Bioprocesses",
        "Elective-I (Nanobiotech / Microbial Biodiversity)"
      ]
    }
  },

  "ME": {
    "CSE": {
      "1": ["Advanced Algorithms", "Machine Learning", "Research Methodology"],
      "2": ["Advanced DBMS", "Data Mining", "Cloud Computing"],
      "3": ["Thesis Phase I", "Seminar"],
      "4": ["Thesis Phase II"]
    },
    "ECE": {
      "1": ["Advanced Signal Processing", "VLSI Design", "Research Methodology"],
      "2": ["Wireless Communication", "Embedded Systems", "Advanced Communication Systems"],
      "3": ["Thesis Phase I", "Seminar"],
      "4": ["Thesis Phase II"]
    },
    "MECH": {
      "1": ["Advanced Thermodynamics", "Finite Element Methods", "Research Methodology"],
      "2": ["Computer-Aided Design", "Mechatronics", "Advanced Manufacturing"],
      "3": ["Thesis Phase I", "Seminar"],
      "4": ["Thesis Phase II"]
    }
  }
};
