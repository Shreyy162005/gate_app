import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max, Avg, Count
from django.db.models.functions import TruncDate
from .models import Student, Test, TestAttempt
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

# SUBJECTS & TOPICS
subjects = {
    1: ["Array", "Linked List", "Tree", "Graph", "Stack", "Queue"],
    2: ["ER Model", "Relational Algebra", "SQL", "Normalization", "Transactions"],
    3: ["Mathematical Logic", "Sets", "Relations", "Functions", "Graph Theory"],
    4: ["Numerical Ability", "Data Interpretation", "Verbal", "Reasoning"],
}

# SUBJECTS & TOPICS
subjects = {
    1: ["Array", "Linked List", "Tree", "Graph", "Stack", "Queue"],
    2: ["ER Model", "Relational Algebra", "SQL", "Normalization", "Transactions"],
    3: ["Mathematical Logic", "Sets", "Relations", "Functions", "Graph Theory"],
    4: ["Numerical Ability", "Data Interpretation", "Verbal", "Reasoning"],
}

questions_data = {
        (1,1): [
        {"q":"Array index starts from?","options":["0","1","-1","2"],"ans":"0"},
        {"q":"Access time in array?","options":["O(1)","O(n)","O(log n)","O(n^2)"],"ans":"O(1)"},
        {"q":"Array is?","options":["Linear","Non-linear","Tree","Graph"],"ans":"Linear"},
        {"q":"Memory allocation?","options":["Contiguous","Random","Linked","None"],"ans":"Contiguous"},
        {"q":"Insertion complexity worst?","options":["O(1)","O(n)","O(log n)","O(n^2)"],"ans":"O(n)"},
        {"q":"Deletion complexity worst?","options":["O(1)","O(n)","O(log n)","O(n^2)"],"ans":"O(n)"},
        {"q":"Search in unsorted array?","options":["O(n)","O(1)","O(log n)","O(n^2)"],"ans":"O(n)"},
        {"q":"Binary search works on?","options":["Sorted array","Unsorted","Tree","Graph"],"ans":"Sorted array"},
        {"q":"Multi-dimensional array?","options":["Yes","No","Maybe","None"],"ans":"Yes"},
        {"q":"Size of array?","options":["Fixed","Dynamic","Both","None"],"ans":"Fixed"},
],

# 2️⃣ Linked List
(1,2): [
        {"q":"Linked list uses?","options":["Pointers","Array","Stack","Queue"],"ans":"Pointers"},
        {"q":"Access time?","options":["O(n)","O(1)","O(log n)","None"],"ans":"O(n)"},
        {"q":"Insertion at beginning?","options":["O(1)","O(n)","O(log n)","None"],"ans":"O(1)"},
        {"q":"Deletion at beginning?","options":["O(1)","O(n)","O(log n)","None"],"ans":"O(1)"},
        {"q":"Memory usage?","options":["More","Less","Same","None"],"ans":"More"},
        {"q":"Traversal type?","options":["Sequential","Random","Both","None"],"ans":"Sequential"},
        {"q":"Types of LL?","options":["SLL","DLL","CLL","All"],"ans":"All"},
        {"q":"Last node points to?","options":["NULL","Start","Middle","None"],"ans":"NULL"},
        {"q":"Search complexity?","options":["O(n)","O(1)","O(log n)","None"],"ans":"O(n)"},
        {"q":"Dynamic size?","options":["Yes","No","None","Maybe"],"ans":"Yes"},
],

# 3️⃣ Tree
(1,3): [
        {"q":"Tree is?","options":["Non-linear","Linear","Array","Stack"],"ans":"Non-linear"},
        {"q":"Root node?","options":["Top","Bottom","Middle","None"],"ans":"Top"},
        {"q":"Binary tree max children?","options":["2","3","4","1"],"ans":"2"},
        {"q":"Height of tree?","options":["Levels","Edges","Nodes","None"],"ans":"Levels"},
        {"q":"Traversal types?","options":["Inorder","Preorder","Postorder","All"],"ans":"All"},
        {"q":"Leaf node?","options":["No child","One child","Two child","None"],"ans":"No child"},
        {"q":"Full binary tree?","options":["0 or 2 children","1 child","None","All"],"ans":"0 or 2 children"},
        {"q":"BST property?","options":["Left<Root<Right","Right<Left","None","All"],"ans":"Left<Root<Right"},
        {"q":"Tree edges for n nodes?","options":["n-1","n","n+1","2n"],"ans":"n-1"},
        {"q":"Balanced tree height?","options":["O(log n)","O(n)","O(n^2)","None"],"ans":"O(log n)"},
],

# 4️⃣ Graph
(1,4): [
{"q":"Graph consists of?","options":["Nodes & edges","Only nodes","Only edges","None"],"ans":"Nodes & edges"},
{"q":"Max edges undirected?","options":["n(n-1)/2","n","n^2","log n"],"ans":"n(n-1)/2"},
{"q":"DFS uses?","options":["Stack","Queue","Array","None"],"ans":"Stack"},
{"q":"BFS uses?","options":["Queue","Stack","Array","None"],"ans":"Queue"},
{"q":"Cycle means?","options":["Loop","Line","Tree","None"],"ans":"Loop"},
{"q":"Directed graph?","options":["Edges with direction","No direction","None","All"],"ans":"Edges with direction"},
{"q":"Graph traversal?","options":["DFS","BFS","Both","None"],"ans":"Both"},
{"q":"Connected graph?","options":["Path exists","No path","None","All"],"ans":"Path exists"},
{"q":"Tree is graph?","options":["Yes","No","Maybe","None"],"ans":"Yes"},
{"q":"Adjacency matrix size?","options":["n x n","n","n/2","None"],"ans":"n x n"},
],

# 5️⃣ Stack
(1,5): [
        {"q":"Stack follows?","options":["LIFO","FIFO","Random","None"],"ans":"LIFO"},
        {"q":"Insertion?","options":["Push","Pop","Peek","None"],"ans":"Push"},
        {"q":"Deletion?","options":["Pop","Push","Peek","None"],"ans":"Pop"},
        {"q":"Top element access?","options":["Peek","Push","Pop","None"],"ans":"Peek"},
        {"q":"Overflow occurs when?","options":["Full","Empty","Half","None"],"ans":"Full"},
        {"q":"Underflow occurs when?","options":["Empty","Full","None","Half"],"ans":"Empty"},
        {"q":"Stack implementation?","options":["Array","LL","Both","None"],"ans":"Both"},
        {"q":"Recursion uses?","options":["Stack","Queue","Array","None"],"ans":"Stack"},
        {"q":"Time complexity push?","options":["O(1)","O(n)","O(log n)","None"],"ans":"O(1)"},
        {"q":"Balanced parentheses uses?","options":["Stack","Queue","Array","None"],"ans":"Stack"},
],

# 6️⃣ Queue
(1,6): [
        {"q":"Queue follows?","options":["FIFO","LIFO","Random","None"],"ans":"FIFO"},
        {"q":"Insertion?","options":["Enqueue","Dequeue","Peek","None"],"ans":"Enqueue"},
        {"q":"Deletion?","options":["Dequeue","Enqueue","Peek","None"],"ans":"Dequeue"},
        {"q":"Front element access?","options":["Peek","Push","Pop","None"],"ans":"Peek"},
        {"q":"Overflow occurs when?","options":["Full","Empty","None","Half"],"ans":"Full"},
        {"q":"Underflow occurs when?","options":["Empty","Full","None","Half"],"ans":"Empty"},
        {"q":"Queue implementation?","options":["Array","LL","Both","None"],"ans":"Both"},
        {"q":"Circular queue solves?","options":["Wastage","Overflow","None","All"],"ans":"Wastage"},
        {"q":"Priority queue?","options":["Priority based","FIFO","LIFO","None"],"ans":"Priority based"},
        {"q":"Time complexity enqueue?","options":["O(1)","O(n)","O(log n)","None"],"ans":"O(1)"},
],


    # ===== 2️⃣ DBMS =====
    (2,1): [
        {"q":"Entity represents?","options":["Object","Attribute","Relation","None"],"ans":"Object"},
        {"q":"Attribute is?","options":["Property","Table","Key","None"],"ans":"Property"},
        {"q":"Primary key must be?","options":["Unique","Duplicate","Null","None"],"ans":"Unique"},
        {"q":"Weak entity depends on?","options":["Strong entity","Relation","Key","None"],"ans":"Strong entity"},
        {"q":"Relationship represents?","options":["Association","Table","Key","None"],"ans":"Association"},
        {"q":"Composite attribute means?","options":["Multiple parts","Single","Derived","None"],"ans":"Multiple parts"},
        {"q":"Derived attribute is?","options":["Calculated","Stored","Primary","None"],"ans":"Calculated"},
        {"q":"ER diagram used for?","options":["Design","Coding","Testing","None"],"ans":"Design"},
        {"q":"Key attribute identifies?","options":["Entity","Relation","Attribute","None"],"ans":"Entity"},
        {"q":"Cardinality defines?","options":["Mapping","Attribute","Entity","None"],"ans":"Mapping"},

    ],


    (2,2): [
        {"q":"Select operation symbol?","options":["σ","π","∪","×"],"ans":"σ"},
        {"q":"Project operation symbol?","options":["π","σ","∪","×"],"ans":"π"},
        {"q":"Union operation requires?","options":["Same schema","Different schema","None","All"],"ans":"Same schema"},
        {"q":"Cartesian product symbol?","options":["×","∪","σ","π"],"ans":"×"},
        {"q":"Join is combination of?","options":["Select+Product","Union","Project","None"],"ans":"Select+Product"},
        {"q":"Difference operation symbol?","options":["-","∪","×","π"],"ans":"-"},
        {"q":"Intersection means?","options":["Common tuples","All tuples","None","Unique"],"ans":"Common tuples"},
        {"q":"Rename operator?","options":["ρ","σ","π","×"],"ans":"ρ"},
        {"q":"Theta join uses?","options":["Condition","Union","Projection","None"],"ans":"Condition"},
        {"q":"Relational algebra works on?","options":["Relations","Tables","Both","None"],"ans":"Both"},
    ],

    (2,3): [
        {"q":"Command to fetch data?","options":["SELECT","GET","FETCH","SHOW"],"ans":"SELECT"},
        {"q":"Clause to filter rows?","options":["WHERE","FROM","SELECT","GROUP"],"ans":"WHERE"},
        {"q":"Primary key allows?","options":["Unique","Duplicate","Null","All"],"ans":"Unique"},
        {"q":"Command to insert data?","options":["INSERT","ADD","PUT","STORE"],"ans":"INSERT"},
        {"q":"Update command?","options":["UPDATE","MODIFY","CHANGE","SET"],"ans":"UPDATE"},
        {"q":"Delete command?","options":["DELETE","REMOVE","DROP","CLEAR"],"ans":"DELETE"},
        {"q":"Group by used for?","options":["Aggregation","Filtering","Sorting","None"],"ans":"Aggregation"},
        {"q":"Order by used for?","options":["Sorting","Filtering","Grouping","None"],"ans":"Sorting"},
        {"q":"Join combines?","options":["Tables","Rows","Columns","None"],"ans":"Tables"},
        {"q":"DDL command?","options":["CREATE","SELECT","INSERT","UPDATE"],"ans":"CREATE"},
    ],

    (2,4): [
        {"q":"Normalization reduces?","options":["Redundancy","Data","Tables","Rows"],"ans":"Redundancy"},
        {"q":"1NF removes?","options":["Repeating groups","Dependency","Keys","None"],"ans":"Repeating groups"},
        {"q":"2NF removes?","options":["Partial dependency","Transitive","Redundancy","None"],"ans":"Partial dependency"},
        {"q":"3NF removes?","options":["Transitive dependency","Partial","Redundancy","None"],"ans":"Transitive dependency"},
        {"q":"BCNF is?","options":["Stronger 3NF","Weaker","Same","None"],"ans":"Stronger 3NF"},
        {"q":"Functional dependency means?","options":["Relation","Attribute relation","Key","None"],"ans":"Attribute relation"},
        {"q":"Prime attribute?","options":["Part of key","Non-key","Derived","None"],"ans":"Part of key"},
        {"q":"Lossless join means?","options":["No data loss","Loss","Duplicate","None"],"ans":"No data loss"},
        {"q":"Decomposition used for?","options":["Normalization","Join","Insert","None"],"ans":"Normalization"},
        {"q":"Candidate key?","options":["Minimal key","Primary","Foreign","None"],"ans":"Minimal key"},
],
    

    (2,5): [
        {"q":"ACID property A?","options":["Atomicity","Access","Apply","None"],"ans":"Atomicity"},
        {"q":"Consistency means?","options":["Valid state","Invalid","None","All"],"ans":"Valid state"},
        {"q":"Isolation ensures?","options":["Independent execution","Together","None","All"],"ans":"Independent execution"},
        {"q":"Durability means?","options":["Permanent","Temporary","None","All"],"ans":"Permanent"},
        {"q":"Deadlock occurs when?","options":["Circular wait","No wait","None","All"],"ans":"Circular wait"},
        {"q":"Lock used for?","options":["Control access","Speed","Memory","None"],"ans":"Control access"},
        {"q":"Two-phase locking ensures?","options":["Serializability","Speed","Deadlock","None"],"ans":"Serializability"},
        {"q":"Rollback means?","options":["Undo","Redo","Save","None"],"ans":"Undo"},
        {"q":"Commit means?","options":["Save","Delete","Undo","None"],"ans":"Save"},
        {"q":"Concurrency control avoids?","options":["Inconsistency","Speed","Memory","None"],"ans":"Inconsistency"},
    ],


    # ===== 3️⃣ ENGINEERING MATHS =====
    (3,1): [
        {"q":"p ∧ q is?","options":["AND","OR","NOT","Implies"],"ans":"AND"},
        {"q":"p ∨ q is?","options":["OR","AND","NOT","Implies"],"ans":"OR"},
        {"q":"Negation of true?","options":["False","True","None","Both"],"ans":"False"},
        {"q":"Implication p→q false when?","options":["T,F","F,T","T,T","F,F"],"ans":"T,F"},
        {"q":"Tautology means?","options":["Always true","Always false","Sometimes","None"],"ans":"Always true"},
        {"q":"Contradiction means?","options":["Always false","Always true","None","Both"],"ans":"Always false"},
        {"q":"p ↔ q means?","options":["Bi-conditional","AND","OR","NOT"],"ans":"Bi-conditional"},
        {"q":"De Morgan law?","options":["Correct","Wrong","None","All"],"ans":"Correct"},
        {"q":"Logical variable values?","options":["True/False","0/1","Both","None"],"ans":"Both"},
        {"q":"Predicate logic deals with?","options":["Statements","Numbers","Graphs","None"],"ans":"Statements"},
            ],

    (3,2): [
        {"q":"Union symbol?","options":["∪","∩","+","-"],"ans":"∪"},
        {"q":"Intersection symbol?","options":["∩","∪","+","-"],"ans":"∩"},
        {"q":"Subset means?","options":["Part","Whole","None","All"],"ans":"Part"},
        {"q":"Universal set?","options":["All elements","Some","None","All"],"ans":"All elements"},
        {"q":"Empty set?","options":["No element","All elements","None","All"],"ans":"No element"},
        {"q":"A ∩ B means?","options":["Common","All","None","Union"],"ans":"Common"},
        {"q":"A ∪ B means?","options":["All","Common","None","Both"],"ans":"All"},
        {"q":"Power set size of n?","options":["2^n","n^2","n","None"],"ans":"2^n"},
        {"q":"Disjoint sets?","options":["No common","Common","All","None"],"ans":"No common"},
        {"q":"Set difference A-B?","options":["A only","B only","Both","None"],"ans":"A only"},
    ],

    (3,3): [
        {"q":"Relation is subset of?","options":["A×B","A","B","None"],"ans":"A×B"},
        {"q":"Reflexive means?","options":["(a,a) present","Not present","None","All"],"ans":"(a,a) present"},
        {"q":"Symmetric means?","options":["(a,b)->(b,a)","(a,a)","None","All"],"ans":"(a,b)->(b,a)"},
        {"q":"Transitive means?","options":["(a,b),(b,c)->(a,c)","None","All","Same"],"ans":"(a,b),(b,c)->(a,c)"},
        {"q":"Equivalence relation?","options":["Ref+Sym+Trans","Only ref","Only sym","None"],"ans":"Ref+Sym+Trans"},
        {"q":"Function is relation?","options":["Yes","No","Maybe","None"],"ans":"Yes"},
        {"q":"Identity relation?","options":["(a,a)","(a,b)","None","All"],"ans":"(a,a)"},
        {"q":"Inverse relation?","options":["Swap pairs","Same","None","All"],"ans":"Swap pairs"},
        {"q":"Relation size?","options":["Number of pairs","Elements","None","All"],"ans":"Number of pairs"},
        {"q":"Relation domain?","options":["First element","Second","None","All"],"ans":"First element"},
    ],
    

    (3,4): [
        {"q":"Function maps?","options":["Input→Output","Output→Input","None","All"],"ans":"Input→Output"},
        {"q":"Injective means?","options":["One-one","Many-one","None","All"],"ans":"One-one"},
        {"q":"Surjective means?","options":["Onto","One-one","None","All"],"ans":"Onto"},
        {"q":"Bijective means?","options":["One-one & onto","Only one","None","All"],"ans":"One-one & onto"},
        {"q":"f(x)=x^2 is?","options":["Many-one","One-one","None","All"],"ans":"Many-one"},
        {"q":"Inverse exists for?","options":["Bijective","Injective","None","All"],"ans":"Bijective"},
        {"q":"Domain means?","options":["Input set","Output","None","All"],"ans":"Input set"},
        {"q":"Range means?","options":["Output set","Input","None","All"],"ans":"Output set"},
        {"q":"Constant function?","options":["Same output","Different","None","All"],"ans":"Same output"},
        {"q":"Composite function?","options":["f(g(x))","g(f(x))","Both","None"],"ans":"Both"},
    ],

    (3,5): [
        {"q":"Graph has?","options":["Vertices & edges","Only nodes","Only edges","None"],"ans":"Vertices & edges"},
        {"q":"Degree of vertex?","options":["Edges count","Nodes","None","All"],"ans":"Edges count"},
        {"q":"Complete graph edges?","options":["n(n-1)/2","n","n^2","None"],"ans":"n(n-1)/2"},
        {"q":"Tree is?","options":["Acyclic graph","Cycle","None","All"],"ans":"Acyclic graph"},
        {"q":"Path means?","options":["Sequence of vertices","Edges","None","All"],"ans":"Sequence of vertices"},
        {"q":"Cycle means?","options":["Closed path","Open","None","All"],"ans":"Closed path"},
        {"q":"Connected graph?","options":["Path exists","No path","None","All"],"ans":"Path exists"},
        {"q":"Bipartite graph?","options":["Two sets","One","None","All"],"ans":"Two sets"},
        {"q":"DFS uses?","options":["Stack","Queue","None","All"],"ans":"Stack"},
        {"q":"BFS uses?","options":["Queue","Stack","None","All"],"ans":"Queue"},
            ],


    # ===== 4️⃣ APTITUDE =====
    (4,1): [
        {"q":"50% of 240?","options":["120","100","140","160"],"ans":"120"},
        {"q":"Simple interest formula?","options":["PTR/100","P+R","P*T","None"],"ans":"PTR/100"},
        {"q":"Average of 10,20,30?","options":["20","15","25","30"],"ans":"20"},
        {"q":"Ratio 4:8=?","options":["1:2","2:1","4:1","None"],"ans":"1:2"},
        {"q":"Speed=Distance/?","options":["Time","Work","Rate","None"],"ans":"Time"},
        {"q":"10% of 500?","options":["50","40","60","30"],"ans":"50"},
        {"q":"LCM of 2,4?","options":["4","2","8","None"],"ans":"4"},
        {"q":"HCF of 6,9?","options":["3","6","9","None"],"ans":"3"},
        {"q":"Profit =?","options":["SP-CP","CP-SP","SP+CP","None"],"ans":"SP-CP"},
        {"q":"Discount means?","options":["Reduction","Addition","None","All"],"ans":"Reduction"},
    ],

    (4,2): [
        
        {"q":"Pie chart shows?","options":["Proportion","Trend","None","All"],"ans":"Proportion"},
        {"q":"Table used for?","options":["Data display","Calculation","None","All"],"ans":"Data display"},
        {"q":"Percentage formula?","options":["(value/total)*100","value+total","None","All"],"ans":"(value/total)*100"},
        {"q":"Average formula?","options":["Sum/n","n/sum","None","All"],"ans":"Sum/n"},
        {"q":"Line graph shows?","options":["Trend","Comparison","None","All"],"ans":"Trend"},
        {"q":"Increase % formula?","options":["(change/original)*100","None","All","Same"],"ans":"(change/original)*100"},
        {"q":"Decrease % formula?","options":["(loss/original)*100","None","All","Same"],"ans":"(loss/original)*100"},
        {"q":"Data interpretation means?","options":["Analyze data","Store data","None","All"],"ans":"Analyze data"},
        {"q":"Units must be?","options":["Same","Different","None","All"],"ans":"Same"},
    ],

    (4,3): [
        {"q":"Synonym of Happy?","options":["Joyful","Sad","Angry","None"],"ans":"Joyful"},
        {"q":"Antonym of 'Increase'?","options":["Decrease","Rise","Grow","None"],"ans":"Decrease"},
        {"q":"Choose correct spelling","options":["Receive","Recieve","Receeve","None"],"ans":"Receive"},
        {"q":"Fill: She ___ going","options":["is","are","am","None"],"ans":"is"},
        {"q":"Noun is?","options":["Name","Action","Quality","None"],"ans":"Name"},
        {"q":"Verb is?","options":["Action","Name","Quality","None"],"ans":"Action"},
        {"q":"Adjective describes?","options":["Noun","Verb","None","All"],"ans":"Noun"},
        {"q":"Adverb describes?","options":["Verb","Noun","None","All"],"ans":"Verb"},
        {"q":"Opposite of 'Fast'?","options":["Slow","Quick","Rapid","None"],"ans":"Slow"},
        {"q":"Sentence correctness?","options":["Grammar","Math","Logic","None"],"ans":"Grammar"},
            ],

    (4,4): [
        {"q":"Odd one out: 2,4,6,9","options":["9","6","4","2"],"ans":"9"},
        {"q":"Series: 2,4,8,16?","options":["32","24","20","None"],"ans":"32"},
        {"q":"A>B, B>C ⇒?","options":["A>C","C>A","None","All"],"ans":"A>C"},
        {"q":"Mirror image tests?","options":["Visual","Math","None","All"],"ans":"Visual"},
        {"q":"Coding: A→1, B→2, C→?","options":["3","2","1","None"],"ans":"3"},
        {"q":"Direction test uses?","options":["Logic","Math","None","All"],"ans":"Logic"},
        {"q":"Blood relation tests?","options":["Family","Math","None","All"],"ans":"Family"},
        {"q":"Venn diagram shows?","options":["Sets","Numbers","None","All"],"ans":"Sets"},
        {"q":"Puzzle solving requires?","options":["Logic","Memory","None","All"],"ans":"Logic"},
        {"q":"Alphabet series: A,C,E?","options":["G","F","H","None"],"ans":"G"},
    ],
}

# REGISTER
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=name, email=email, password=password)
        # Create Student instance
        Student.objects.create(user=user)
        return redirect("login")

    return render(request, "register.html")


# LOGIN
def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        # Authenticate using username and password
        user = authenticate(request, username=name, password=password)

        if user:
            login(request, user)
            # Redirect superuser to faculty dashboard
            if user.is_superuser:
                return redirect("faculty_dashboard")
            else:
                return redirect("home")
        else:
            error_msg = "Invalid username or password. Please try again."
            return render(request, "login.html", {"error": error_msg})

    return render(request, "login.html")


# HOME
@login_required
def home(request):
    return render(request, "home.html")


# TOPICS
@login_required
def topics(request, subject_id):
    return render(request, "topics.html", {
        "topics": subjects.get(subject_id, []),
        "subject_id": subject_id
    })


# TEST
@login_required
def test(request, test_id):
    try:
        subject_id, topic_id = map(int, test_id.split("_"))
    except (ValueError, TypeError):
        return redirect("home")

    questions = questions_data.get((subject_id, topic_id), [])
    if not questions:
        return redirect("home")

    # Create Test if not exists
    test_name = f"{subjects[subject_id][topic_id-1]} ({subject_id}.{topic_id})"
    test_obj, created = Test.objects.get_or_create(
        name=test_name,
        defaults={'subject_id': subject_id, 'topic_id': topic_id}
    )

    return render(request, "test.html", {
        "questions": questions,
        "test_id": test_id,
        "test_obj": test_obj
    })


# RESULT
@login_required
def result(request):
    if request.method != "POST":
        return render(request, "result.html", {
            "error": "Please submit the test from the test page to see the result."
        })

    test_id = request.POST.get("test_id")
    if not test_id:
        return render(request, "result.html", {
            "error": "No test identifier was submitted. Please retry the test."
        })

    try:
        subject_id, topic_id = map(int, test_id.split("_"))
    except (ValueError, TypeError, AttributeError):
        return render(request, "result.html", {
            "error": "Invalid test identifier. Please retry the test."
        })

    questions = questions_data.get((subject_id, topic_id), [])
    if not questions:
        return render(request, "result.html", {
            "error": "Test questions could not be found. Please retry the test."
        })

    score = 0
    total = len(questions)
    result_data = []

    for i, q in enumerate(questions):
        user_ans = request.POST.get(str(i))
        correct = q["ans"]

        if user_ans == correct:
            score += 1

        result_data.append({
            "question": q["q"],
            "user_ans": user_ans,
            "correct_ans": correct
        })

    percent = (score / total) * 100 if total else 0

    # Save TestAttempt
    try:
        student = Student.objects.get(user=request.user)
        test_name = f"{subjects[subject_id][topic_id-1]} ({subject_id}.{topic_id})"
        test_obj = Test.objects.get(name=test_name)
        TestAttempt.objects.create(
            student=student,
            test=test_obj,
            score=score,
            total=total
        )
    except (Student.DoesNotExist, Test.DoesNotExist):
        pass  # Handle silently or log

    return render(request, "result.html", {
        "score": score,
        "total": total,
        "percent": percent,
        "data": result_data
    })

@user_passes_test(is_superuser)
def faculty_dashboard(request):

    total_students = Student.objects.count()

    top_performers = Student.objects.annotate(
        max_score=Max('testattempt__score')
    ).order_by('-max_score')[:5]

    attempts = TestAttempt.objects.select_related(
        'student__user', 'test'
    ).order_by('-date_time')

    # ✅ Average score (NEW FIX)
    avg_score = TestAttempt.objects.aggregate(avg=Avg('score'))['avg'] or 0
    avg_score = round(avg_score, 1)

    # Charts
    top_scores_labels = [p.user.username for p in top_performers]
    top_scores_data = [p.max_score or 0 for p in top_performers]

    last_30_days = timezone.now() - timedelta(days=30)

    daily_avg = TestAttempt.objects.filter(
        date_time__gte=last_30_days
    ).annotate(
        day=TruncDate('date_time')
    ).values('day').annotate(
        avg_score=Avg('score')
    ).order_by('day')

    line_labels = [str(d['day']) for d in daily_avg]
    line_data = [float(d['avg_score']) for d in daily_avg]

    context = {
        'total_students': total_students,
        'top_performers': top_performers,
        'attempts': attempts,
        'avg_score': avg_score,   # ✅ IMPORTANT
        'top_scores_labels': json.dumps(top_scores_labels),
        'top_scores_data': json.dumps(top_scores_data),
        'line_labels': json.dumps(line_labels),
        'line_data': json.dumps(line_data),
    }

    return render(request, 'faculty_dashboard.html', context)

from django.http import JsonResponse

@user_passes_test(is_superuser)
def student_performance(request, student_id):
    attempts = TestAttempt.objects.filter(
        student_id=student_id
    ).order_by('date_time')

    labels = []
    scores = []

    for a in attempts:
        labels.append(a.test.name)
        scores.append(a.score)

    return JsonResponse({
        "labels": labels,
        "scores": scores
    })
