from github import Github
import base64
import streamlit as st
import random
from datetime import datetime

# ==========================================
# 1. GITHUB CLOUD STORAGE SETUP
# ==========================================
def save_score_to_github():
    # Retrieve secrets set up in Streamlit Cloud
    token = st.secrets["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"]
    repo_name = st.secrets["warehouse-tycoon"]
    file_path = "student_scores.csv"

    g = Github(token)
    repo = g.get_repo(repo_name)

    # Format the student data as a comma-separated row
    date_played = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = f"{st.session_state.student['name']},{st.session_state.student['email']},{st.session_state.student['roll_no']},{st.session_state.student['class']},{st.session_state.student['division']},{st.session_state.score},{st.session_state.level},{date_played}\n"

    try:
        # Check if the file already exists in the repository
        contents = repo.get_contents(file_path)
        decoded_content = base64.b64decode(contents.content).decode("utf-8")
        updated_content = decoded_content + new_row
        
        # Update the existing file
        repo.update_file(contents.path, "Added new student score", updated_content, contents.sha)
    except:
        # If the file does not exist, create it with a header row
        header = "Name,Email,Roll_No,Class,Division,Score,Rank,Date\n"
        updated_content = header + new_row
        repo.create_file(file_path, "Created scores file", updated_content)


# ==========================================
# 2. DYNAMIC QUESTION ENGINE
# ==========================================
class Question:
    def __init__(self, q_text, options, correct_option_text, q_type, difficulty, explanation):
        self.q_text = q_text
        self.q_type = q_type
        self.difficulty = difficulty
        self.explanation = explanation
        self.options = options.copy()
        random.shuffle(self.options)
        self.correct_index = self.options.index(correct_option_text)

class TemplateBank:
    @staticmethod
    def generate(score):
        if score < 150:
            return TemplateBank.get_beginner()
        elif 150 <= score < 400:
            return TemplateBank.get_intermediate()
        else:
            return TemplateBank.get_advanced()

    @staticmethod
    def get_beginner():
        templates = [
            # 1. Data Marts
            lambda: Question(
                q_text=f"Your manager at {random.choice(['TechCorp', 'Global Retail', 'EduTech'])} wants a specialized database set up in {random.choice(['6 weeks', '3 months', '4 weeks'])} for the {random.choice(['HR', 'Marketing', 'Finance'])} team. What should you build?",
                options=["Enterprise Data Warehouse", "Galaxy Schema", "Data Mart", "Landing Area"],
                correct_option_text="Data Mart",
                q_type="Architecture", difficulty="Beginner",
                explanation="A Data Mart is a specialized subset of a data warehouse, limited in scope to a single business domain, and can be deployed quickly."
            ),
            # 2. OLAP vs OLTP
            lambda: Question(
                q_text=f"Which system is engineered for {random.choice(['analysts', 'managers', 'executives'])} to perform {random.choice(['deep, read-heavy', 'complex, ad-hoc'])} calculations over massive datasets?",
                options=["OLTP", "OLAP", "3NF Operational Database", "Data Lake"],
                correct_option_text="OLAP",
                q_type="Concept", difficulty="Beginner",
                explanation="OLAP (Online Analytical Processing) workloads are engineered for deep, read-heavy analytical calculations."
            ),
            # 3. DW Characteristics - Integrated
            lambda: Question(
                q_text="According to Bill Inmon, data gathered from multiple heterogeneous sources must be cleaned and transformed into a consistent format. Which characteristic of a Data Warehouse does this describe?",
                options=["Subject-Oriented", "Integrated", "Time-Variant", "Non-Volatile"],
                correct_option_text="Integrated",
                q_type="Concept", difficulty="Beginner",
                explanation="Integrated means data is gathered from different sources and transformed to resolve conflicts and establish a unified format."
            ),
            # 4. Fact Tables
            lambda: Question(
                q_text=f"In a retail dimensional model, a table stores numeric metrics like {random.choice(['sales_amount and discount', 'quantity_sold and tax_amount'])}. What type of table is this?",
                options=["Dimension Table", "Fact Table", "Bridge Table", "Lookup Table"],
                correct_option_text="Fact Table",
                q_type="Dimensional Modeling", difficulty="Beginner",
                explanation="Fact tables store the measurable, quantitative data (metrics) about a business event."
            ),
            # 5. Dimension Tables
            lambda: Question(
                q_text=f"You need to store descriptive attributes such as {random.choice(['customer_name, age, and address', 'product_category, brand, and weight'])}. Where should this data go?",
                options=["Fact Table", "Dimension Table", "Surrogate Key Table", "Factless Fact Table"],
                correct_option_text="Dimension Table",
                q_type="Dimensional Modeling", difficulty="Beginner",
                explanation="Dimension tables store the textual, descriptive context (the 'who, what, where, when') of business events."
            ),
            # 6. DW Characteristics - Non-Volatile
            lambda: Question(
                q_text="Once data is loaded into a Data Warehouse, it is generally not updated or deleted by normal transactional processes. Which characteristic does this describe?",
                options=["Subject-Oriented", "Integrated", "Time-Variant", "Non-Volatile"],
                correct_option_text="Non-Volatile",
                q_type="Concept", difficulty="Beginner",
                explanation="Non-Volatile means historical data is preserved and not overwritten by day-to-day operations."
            ),
            # 7. Star Schema Basics
            lambda: Question(
                q_text="Which schema features a single central fact table directly connected to multiple heavily denormalized dimension tables, resembling a specific celestial shape?",
                options=["Snowflake Schema", "Star Schema", "Galaxy Schema", "3rd Normal Form"],
                correct_option_text="Star Schema",
                q_type="Architecture", difficulty="Beginner",
                explanation="A Star Schema has one central fact table connected to denormalized dimensions, optimizing read performance."
            ),
            # 8. ETL - Extract
            lambda: Question(
                q_text=f"The first step of your data pipeline involves pulling raw {random.choice(['JSON files from an API', 'records from a MySQL database'])} without altering the data. Which phase is this?",
                options=["Extract", "Transform", "Load", "Cleansing"],
                correct_option_text="Extract",
                q_type="ETL", difficulty="Beginner",
                explanation="The Extract phase simply reads and pulls raw data from source systems into a staging area."
            )
        ]
        return random.choice(templates)()

    @staticmethod
    def get_intermediate():
        templates = [
            # 1. Snowflake Schema
            lambda: Question(
                q_text=f"To save disk storage, an architect normalized the {random.choice(['Dim_Product', 'Dim_Location'])} table into multiple branching sub-dimension tables. What schema pattern was just created?",
                options=["Star Schema", "Snowflake Schema", "Galaxy Schema", "Factless Fact Table"],
                correct_option_text="Snowflake Schema",
                q_type="Architecture", difficulty="Intermediate",
                explanation="A Snowflake Schema normalizes dimension tables into multiple related sub-dimension tables."
            ),
            # 2. ETL - Transform
            lambda: Question(
                q_text=f"During an ETL pipeline, you run a script that {random.choice(['converts all currencies to USD', 'replaces NULL values with standard default strings'])}. Which phase is this?",
                options=["Extract", "Transform", "Load", "Aggregation"],
                correct_option_text="Transform",
                q_type="ETL", difficulty="Intermediate",
                explanation="The Transform phase handles data cleaning, standardization, currency conversions, and handling missing values."
            ),
            # 3. Conformed Dimensions
            lambda: Question(
                q_text="You have a 'Dim_Date' table and a 'Dim_Customer' table that are used by both the Sales Fact Table and the Support Fact Table. What are these shared dimensions called?",
                options=["Degenerate Dimensions", "Junk Dimensions", "Conformed Dimensions", "Role-Playing Dimensions"],
                correct_option_text="Conformed Dimensions",
                q_type="Dimensional Modeling", difficulty="Intermediate",
                explanation="Conformed dimensions are built once and shared across multiple fact tables to ensure consistency across the enterprise."
            ),
            # 4. Factless Fact Tables
            lambda: Question(
                q_text=f"You need to track {random.choice(['student attendance in a class', 'employee login events'])}. The event happens, but there are no numeric metrics (like price or quantity) to record. What should you use?",
                options=["Snapshot Fact Table", "Factless Fact Table", "Bridge Table", "Junk Dimension"],
                correct_option_text="Factless Fact Table",
                q_type="Dimensional Modeling", difficulty="Intermediate",
                explanation="A Factless Fact Table records events or coverage that have no measurable numeric facts, only foreign keys to dimensions."
            ),
            # 5. Degenerate Dimensions
            lambda: Question(
                q_text=f"You have a {random.choice(['Receipt_Number', 'Order_ID'])} that is unique to a transaction. It belongs in the fact table, but it has no other descriptive attributes, so it doesn't need its own dimension table. What is this called?",
                options=["Surrogate Key", "Degenerate Dimension", "Conformed Dimension", "Primary Key"],
                correct_option_text="Degenerate Dimension",
                q_type="Dimensional Modeling", difficulty="Intermediate",
                explanation="A Degenerate Dimension is a dimension key in the fact table that does not have its own dimension table because it has no additional attributes."
            ),
            # 6. Surrogate Keys
            lambda: Question(
                q_text="Instead of using a customer's Social Security Number as the primary key in a dimension table, the architect uses a system-generated integer (1, 2, 3...). What is this key called?",
                options=["Natural Key", "Business Key", "Surrogate Key", "Foreign Key"],
                correct_option_text="Surrogate Key",
                q_type="Database Design", difficulty="Intermediate",
                explanation="Surrogate Keys are meaningless, system-generated integers used as primary keys in dimension tables to insulate the warehouse from operational changes."
            ),
            # 7. Junk Dimension
            lambda: Question(
                q_text=f"A source system has 5 different low-cardinality flags (e.g., {random.choice(['is_active, has_discount, is_premium', 'cash_payment, online_order, gift_wrapped'])}). To avoid cluttering the fact table with 5 separate foreign keys, you combine all combinations into one dimension. What is this called?",
                options=["Degenerate Dimension", "Junk Dimension", "Role-playing Dimension", "Factless Fact Table"],
                correct_option_text="Junk Dimension",
                q_type="Dimensional Modeling", difficulty="Intermediate",
                explanation="A Junk Dimension groups low-cardinality flags and indicators into a single table to save space and simplify the fact table."
            ),
            # 8. Kimball vs Inmon
            lambda: Question(
                q_text="Which Data Warehouse methodology advocates for a 'Bottom-Up' approach, starting with individual departmental Data Marts (using dimensional modeling) that eventually form the enterprise warehouse?",
                options=["Inmon Methodology", "Kimball Methodology", "Data Vault", "Agile BI"],
                correct_option_text="Kimball Methodology",
                q_type="Methodology", difficulty="Intermediate",
                explanation="Ralph Kimball's methodology is bottom-up, focusing on building star-schema Data Marts first."
            )
        ]
        return random.choice(templates)()

    @staticmethod
    def get_advanced():
        templates = [
            # 1. SCD Type 2
            lambda: Question(
                q_text=f"A customer named {random.choice(['Alice', 'Bob'])} moves from New York to London. To track this change for historical accuracy, you add a NEW ROW with a start_date, end_date, and active_flag. Which technique is this?",
                options=["SCD Type 1", "SCD Type 2", "SCD Type 3", "SCD Type 6"],
                correct_option_text="SCD Type 2",
                q_type="Historical Tracking", difficulty="Advanced",
                explanation="Type 2 creates a new row to maintain a complete historical trail of dimension changes over time."
            ),
            # 2. SCD Type 1
            lambda: Question(
                q_text=f"An employee corrects a spelling mistake in their name from '{random.choice(['Jhon to John', 'Smyth to Smith'])}'. You don't need historical tracking, so you simply OVERWRITE the old record. Which technique is this?",
                options=["SCD Type 1", "SCD Type 2", "SCD Type 3", "SCD Type 4"],
                correct_option_text="SCD Type 1",
                q_type="Historical Tracking", difficulty="Advanced",
                explanation="Type 1 Overwrites the existing data. It is easy to implement but destroys historical context."
            ),
            # 3. SCD Type 3
            lambda: Question(
                q_text="A sales region is reassigned. You want to see current sales under the new region, but also be able to map it to the old region. You add a 'Previous_Region' column to the existing row. Which technique is this?",
                options=["SCD Type 1", "SCD Type 2", "SCD Type 3", "SCD Type 6"],
                correct_option_text="SCD Type 3",
                q_type="Historical Tracking", difficulty="Advanced",
                explanation="Type 3 adds a new column (e.g., Previous_Value) to keep a partial history (usually just the most recent change)."
            ),
            # 4. OLAP - Pivot
            lambda: Question(
                q_text=f"An executive is viewing a sales cube. They {random.choice(['swap the rows and columns', 'reorient the axes'])} of the report to get an alternative visual perspective without changing the data. Which OLAP operation was used?",
                options=["Slice", "Dice", "Pivot (Rotation)", "Roll-Up"],
                correct_option_text="Pivot (Rotation)",
                q_type="OLAP Operations", difficulty="Advanced",
                explanation="Pivot (Rotation) reorients the visual representation of the data cube by swapping rows and columns."
            ),
            # 5. OLAP - Roll-up
            lambda: Question(
                q_text="A BI dashboard currently shows 'Daily Sales'. The manager clicks a button to view 'Monthly Sales' instead, reducing the level of detail. Which OLAP operation is this?",
                options=["Drill-Down", "Roll-Up", "Slice", "Dice"],
                correct_option_text="Roll-Up",
                q_type="OLAP Operations", difficulty="Advanced",
                explanation="Roll-up (or consolidation) aggregates the data by climbing up a concept hierarchy (e.g., Day -> Month -> Year)."
            ),
            # 6. OLAP - Drill-down
            lambda: Question(
                q_text="A user is looking at total sales for the 'Electronics' category. They click on it to reveal sales for 'Laptops', 'Phones', and 'Tablets'. Which OLAP operation is this?",
                options=["Drill-Down", "Roll-Up", "Slice", "Dice"],
                correct_option_text="Drill-Down",
                q_type="OLAP Operations", difficulty="Advanced",
                explanation="Drill-down navigates from highly summarized data to more detailed, granular data."
            ),
            # 7. OLAP - Slice
            lambda: Question(
                q_text=f"You have a 3D data cube (Time, Product, Location). You filter the data to ONLY look at the year {random.choice(['2022', '2023'])}, resulting in a 2D table. Which OLAP operation is this?",
                options=["Slice", "Dice", "Pivot", "Roll-Up"],
                correct_option_text="Slice",
                q_type="OLAP Operations", difficulty="Advanced",
                explanation="Slice performs a selection on ONE dimension of a given cube, yielding a subcube (or 2D table)."
            ),
            # 8. Fact Table Types
            lambda: Question(
                q_text="An e-commerce company needs to track the exact lifecycle of an order: Order Placed -> Shipped -> Delivered. They use a fact table with multiple date columns that get updated as the order progresses. What type of fact table is this?",
                options=["Transaction Fact Table", "Periodic Snapshot Fact Table", "Accumulating Snapshot Fact Table", "Factless Fact Table"],
                correct_option_text="Accumulating Snapshot Fact Table",
                q_type="Dimensional Modeling", difficulty="Advanced",
                explanation="Accumulating Snapshot Fact Tables are used for workflows or pipelines where an entity progresses through a series of well-defined steps."
            )
        ]
        
    @staticmethod
    def get_critical_thinking():
        templates = [
            
            # ==========================================
            # CRITICAL THINKING: ARCHITECTURE TRADE-OFFS (ETL vs ELT)
            # ==========================================
            lambda: Question(
                q_text=f"Your team at a {random.choice(['healthcare provider', 'fintech startup', 'government agency'])} wants to migrate to a modern cloud data warehouse and switch to an ELT approach. However, strict compliance rules state that no unmasked {random.choice(['patient health records (PHI)', 'credit card numbers (PCI)', 'citizen social security numbers'])} can EVER touch the warehouse's storage layer, even temporarily. What is the correct architectural decision?",
                options=[
                    "Stick with ETL, masking the data on a separate secure server before it reaches the warehouse.",
                    "Use ELT, but write a SQL script in the warehouse to mask the data immediately after loading.",
                    "Use ELT, but encrypt the cloud warehouse storage volume.",
                    "Bypass the warehouse entirely and use an OLTP database for reporting."
                ],
                correct_option_text="Stick with ETL, masking the data on a separate secure server before it reaches the warehouse.",
                q_type="Critical Thinking: Architecture", difficulty="Advanced",
                explanation="A tightly regulated system requires that no unmasked personal data ever touches the warehouse's storage layer, even temporarily, which means transformation (masking) must happen in an upstream ETL server."
            ),
            
            # ==========================================
            # CRITICAL THINKING: SYSTEM BOTTLENECKS (OLAP vs OLTP)
            # ==========================================
            lambda: Question(
                q_text=f"The VP of Sales at a {random.choice(['global e-commerce platform', 'major airline', 'stock brokerage'])} asks you to point a massive, resource-heavy BI dashboard directly at the live operational database to get 'real-time' insights. Why is this structurally a terrible idea?",
                options=[
                    "Running heavy analytical queries directly against an OLTP system risks slowing down or locking real customer transactions.",
                    "The operational database does not have enough storage space for a dashboard.",
                    "Dashboards cannot connect to normalized 3NF databases.",
                    "The data in the operational database is usually encrypted and cannot be queried."
                ],
                correct_option_text="Running heavy analytical queries directly against an OLTP system risks slowing down or locking real customer transactions.",
                q_type="Critical Thinking: Systems", difficulty="Advanced",
                explanation="OLTP systems handle day-to-day transaction processing; running heavy analytical queries directly against this system risks slowing down real customer checkouts or operations[cite: 1]."
            ),

            # ==========================================
            # CRITICAL THINKING: DIMENSIONAL MODELING GRAIN
            # ==========================================
            lambda: Question(
                q_text=f"You are designing a Star Schema for a {random.choice(['retail chain', 'logistics firm'])}. A junior developer suggests putting {random.choice(['daily individual sales transactions', 'daily individual package shipments'])} and {random.choice(['monthly store rent expenses', 'monthly warehouse utility bills'])} into the EXACT SAME fact table to save space. What fundamental rule of dimensional design does this violate?",
                options=[
                    "Declaring a single, consistent grain.",
                    "Identifying the dimensions.",
                    "Using surrogate keys.",
                    "Creating conformed dimensions."
                ],
                correct_option_text="Declaring a single, consistent grain.",
                q_type="Critical Thinking: Modeling", difficulty="Advanced",
                explanation="Kimball's dimensional design method requires declaring the grain (e.g., one row per line item per transaction) as a crucial early step[cite: 1]. Mixing daily atomic transactions with monthly aggregated expenses in one table makes the data impossible to query accurately."
            ),

            # ==========================================
            # CRITICAL THINKING: SCD TRADE-OFFS (Type 4 vs Type 2)
            # ==========================================
            lambda: Question(
                q_text=f"A {random.choice(['telecom', 'SaaS', 'insurance'])} company has a massive customer dimension table. A performance-sensitive dashboard must query ONLY current-state rows extremely quickly, but auditors simultaneously require a separate, rigorous historical trail of every past change. Which Slowly Changing Dimension strategy handles this specific dual-requirement best?",
                options=[
                    "SCD Type 4", 
                    "SCD Type 1", 
                    "SCD Type 2", 
                    "SCD Type 3"
                ],
                correct_option_text="SCD Type 4",
                q_type="Critical Thinking: Historical Tracking", difficulty="Advanced",
                explanation="SCD Type 4 is ideal here because the current row stays in a lean, fast main table for daily reporting, while a separate history table supports slower historical investigations[cite: 1]."
            ),

            # ==========================================
            # CRITICAL THINKING: OLAP DRILL-ACROSS
            # ==========================================
            lambda: Question(
                q_text=f"An executive at a {random.choice(['manufacturing', 'retail', 'software'])} company needs to compare {random.choice(['units produced against units defective', 'units sold against units returned', 'licenses sold against support tickets raised'])}. These two metrics live in completely separate fact tables built at different grains. How can you compare them side-by-side?",
                options=[
                    "Use a Drill-Across operation via their shared conformed dimensions.",
                    "Use a Drill-Through operation to the OLTP database.",
                    "Use a Slice operation to isolate the metrics.",
                    "It is impossible; they must be merged into a single fact table first."
                ],
                correct_option_text="Use a Drill-Across operation via their shared conformed dimensions.",
                q_type="Critical Thinking: OLAP", difficulty="Advanced",
                explanation="Drill-Across allows two fact tables built at different grains to still be compared side by side using only the dimensions they conform on (like Time or Product)[cite: 1]."
            ),
            
            # ==========================================
            # CRITICAL THINKING: DATA PIPELINE LIFECYCLE
            # ==========================================
            lambda: Question(
                q_text=f"A customer's {random.choice(['city', 'marital status', 'subscription tier'])} just changed in the source system. In what order should the pipeline handle a Type 2 SCD update?",
                options=[
                    "Detect change -> End-date old row -> Generate new surrogate key -> Insert new row.",
                    "Generate new surrogate key -> Detect change -> Insert new row -> Delete old row.",
                    "Insert new row -> End-date old row -> Detect change -> Overwrite surrogate key.",
                    "Detect change -> Overwrite old row -> Generate surrogate key -> Archive old data."
                ],
                correct_option_text="Detect change -> End-date old row -> Generate new surrogate key -> Insert new row.",
                q_type="Critical Thinking: Pipeline Logic", difficulty="Advanced",
                explanation="To trace a Type 2 SCD update logically: Change Data Capture detects the change, the existing row's end_date is set, a new surrogate key is generated, and finally the new row is inserted with its active_flag set to True[cite: 1]."
            )
        ]
        return random.choice(templates)()

# ==========================================
# 3. STREAMLIT UI & GAME STATE
# ==========================================
# Page config for a wide, attractive layout
st.set_page_config(page_title="Warehouse Tycoon", page_icon="🏢", layout="centered")

# Initialize Session State Variables (so data isn't lost on button clicks)
if 'page' not in st.session_state:
    st.session_state.page = 'registration'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'q_num' not in st.session_state:
    st.session_state.q_num = 1
if 'TOTAL_QUESTIONS' not in st.session_state:
    st.session_state.TOTAL_QUESTIONS = 100
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'level' not in st.session_state:
    st.session_state.level = "Junior Analyst (Beginner)"

def update_level():
    # Update title dynamically based on the 4 tiers of scoring
    if st.session_state.score < 150:
        st.session_state.level = "Junior Analyst (Beginner)"
    elif 150 <= st.session_state.score < 300:
        st.session_state.level = "ETL Engineer (Intermediate)"
    elif 300 <= st.session_state.score < 450:
        st.session_state.level = "Data Architect (Advanced)"
    else:
        st.session_state.level = "Principal Architect (Expert)"

# --- PAGE 1: REGISTRATION FORM ---
if st.session_state.page == 'registration':
    st.title("🏢 Warehouse Tycoon: The Architecture Exam")
    st.markdown("Welcome! Please register to begin your 100-question certification exam.")
    
    with st.form("student_form"):
        st.subheader("Student Details")
        name = st.text_input("Full Name")
        email = st.text_input("College Email ID")
        roll_no = st.text_input("Roll Number")
        col1, col2 = st.columns(2)
        with col1:
            student_class = st.text_input("Class (e.g., TYBSc IT)")
        with col2:
            division = st.text_input("Division (e.g., A)")
            
        submitted = st.form_submit_button("Start Exam 🚀")
        
        if submitted:
            if name and email and roll_no and student_class and division:
                st.session_state.student = {
                    'name': name, 'email': email, 'roll_no': roll_no, 
                    'class': student_class, 'division': division
                }
                st.session_state.page = 'game'
                st.rerun() # Refresh the page to load the game
            else:
                st.error("Please fill in all fields to proceed!")

# --- PAGE 2: THE GAME EXAM ---
elif st.session_state.page == 'game':
    update_level()
    
    # Top Dashboard Banner
    col1, col2, col3 = st.columns(3)
    col1.metric("Player", st.session_state.student['name'])
    col2.metric("Current Score", st.session_state.score)
    col3.metric("Rank", st.session_state.level)
    
    # Progress Bar
    progress = st.session_state.q_num / st.session_state.TOTAL_QUESTIONS
    st.progress(progress, text=f"Question {st.session_state.q_num} of {st.session_state.TOTAL_QUESTIONS}")
    st.divider()

    # Generate or Fetch current question
    if st.session_state.current_q is None:
        st.session_state.current_q = TemplateBank.generate(st.session_state.score)

    q = st.session_state.current_q

    # Display Question Tags
    st.caption(f"**Category:** {q.q_type} | **Difficulty:** {q.difficulty}")
    st.subheader(q.q_text)

    # Form to handle answers
    with st.form("answer_form"):
        user_choice = st.radio("Select your answer:", q.options, index=None)
        submit_answer = st.form_submit_button("Submit Answer")

        if submit_answer and user_choice and not st.session_state.answered:
            st.session_state.answered = True
            
            # Check correctness based on text match
            if user_choice == q.options[q.correct_index]:
                st.session_state.score += 10
                st.session_state.correct_flag = True
            else:
                st.session_state.score -= 5
                st.session_state.correct_flag = False
            st.rerun()
        elif submit_answer and not user_choice:
            st.warning("Please select an option before submitting.")

    # Show results and next button ONLY after answering
    if st.session_state.answered:
        if st.session_state.correct_flag:
            st.success("✅ Correct! +10 Points")
        else:
            correct_ans = q.options[q.correct_index]
            st.error(f"❌ Incorrect. -5 Points. The correct answer was: **{correct_ans}**")
            
        st.info(f"**Explanation:** {q.explanation}")
        
        if st.button("Next Question ➡️"):
            if st.session_state.q_num >= st.session_state.TOTAL_QUESTIONS:
                st.session_state.page = 'game_over'
            else:
                st.session_state.q_num += 1
                st.session_state.current_q = None
                st.session_state.answered = False
            st.rerun()

# --- PAGE 3: GAME OVER & SAVE ---
# ==========================================
# 1. GITHUB CLOUD STORAGE SETUP
# ==========================================
def save_score_to_github():
    # Retrieve secrets set up in Streamlit Cloud
    token = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["REPO_NAME"]
    file_path = "student_scores.csv"

    g = Github(token)
    repo = g.get_repo(repo_name)

    # Format the student data as a comma-separated row
    date_played = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = f"{st.session_state.student['name']},{st.session_state.student['email']},{st.session_state.student['roll_no']},{st.session_state.student['class']},{st.session_state.student['division']},{st.session_state.score},{st.session_state.level},{date_played}\n"

    try:
        # Check if the file already exists in the repository
        contents = repo.get_contents(file_path)
        decoded_content = base64.b64decode(contents.content).decode("utf-8")
        updated_content = decoded_content + new_row
        
        # Update the existing file
        repo.update_file(contents.path, "Added new student score", updated_content, contents.sha)
    except:
        # If the file does not exist, create it with a header row
        header = "Name,Email,Roll_No,Class,Division,Score,Rank,Date\n"
        updated_content = header + new_row
        repo.create_file(file_path, "Created scores file", updated_content)
