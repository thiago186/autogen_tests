import autogen

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST.json")


timeout_time = 500

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 5, "work_dir": "group_chat"},
    human_input_mode="ALWAYS",
    llm_config={"config_list": config_list, 'request_timeout': timeout_time}
)

designer = autogen.AssistantAgent(
    name="Designer",
    system_message="As a UI designer, develop visual designs for the screens outlined by the software architect. Choose appropriate color schemes, typography, layout, and graphical elements to create an aesthetically pleasing and user-friendly interface. Your designs should align with the project's overall theme and usability goals.",
    llm_config={"config_list": config_list, 'request_timeout': timeout_time}
)

frontend_dev = autogen.AssistantAgent(
    name="Frontend_Developer",
    system_message="As a frontend developer, create the project files as described by the software architect. Implement the screens, buttons, and other user interface elements according to the provided specifications. Ensure that the code is clean, well-documented, and follows the best practices for frontend development. ALWAYS use react.js in the project and react-routers if needed.",
    llm_config={"config_list": config_list, 'request_timeout': timeout_time}
)

software_architect = autogen.AssistantAgent(
    name="Software_Architect",
    system_message="As a software architect, receives the users whishes and describe the structure of the frontend project, including atomic architecture, folder organization, screens, buttons, and other user interfaces. Provide detailed guidelines to the frontend developer on how these elements should be structured and interrelated to create an efficient and scalable frontend application.",
    llm_config={"config_list": config_list, 'request_timeout': timeout_time}
)

product_manager = autogen.AssistantAgent(
    name="Product_Manager",
    system_message="As a product manager, you are responsible for the product planning and execution. Your job is to receive the software architect's description of the frontend project and send parts of it to the frontend developer. You should also receive the UI designer's visual designs and send them to the frontend developer. You need to control what the frontend developer have already done and what he yet needs to do.",
    llm_config={"config_list": config_list, 'timeout': timeout_time}
)


group_manager_system_message = """
A group chat manager. It never sends the message of a participant to itself. Its objective is to orchestrate the group chat. If the conversation has ended, just says TERMINATE.
The chatflow is the following: 
the UserProxy message goes directly to the SoftwareArchitect.
The SoftwareArchitect message goes to the UI Designer.
The UI Designer message, together with the SoftwareArchitect message, goes to the ProductManager.
The ProductManager controls the execution of the process sending parts of the functionalities to be developed by the FrontendDeveloper.
"""
groupchat = autogen.GroupChat(agents = [user_proxy, designer, frontend_dev, software_architect, product_manager], messages=[], max_round=12)
group_manager = autogen.GroupChatManager(
    system_message= group_manager_system_message,
    groupchat=groupchat,
    llm_config={"config_list": config_list, 'request_timeout': timeout_time}
)

query = ''' 
Create an website with: 
1- login page. The login should be made with email and password.
2- 404 not found page. it should only contain the text "oops, we couldn't find this page :("
3- a home page for authenticated users. it should only contains a simple text for logged users. 

- if a user not authenticated tries to access the home page, it should be redirected to the login page. 
- all pages needs to have a navbar.
'''


# user_proxy.initiate_chat(recipient=product_manager, message=" Hi! How are you?")
user_proxy.initiate_chat(group_manager, message=query)
