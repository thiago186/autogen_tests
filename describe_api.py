import autogen

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST.json")


user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "group_chat"},
    human_input_mode="TERMINATE"
)

cto = autogen.AssistantAgent(
    name="Chief_Technology_Office",
    system_message="A CTO of the company, its responsibility is to maintain contact with PMs to ensure the execution of the project. CTO is always responsible for approving the final project",
    llm_config={"config_list": config_list}
)

pm = autogen.AssistantAgent(
    name="Product_Manager",
    system_message=(
        "A PM of the company, its responsibility is to determine the product requirements and maintain contact with CTOs to ensure the execution of the project. The PM will receive a project and plan all the stack and project arquitecture and requirements.",
        "Every time the PM plans a project, it should pass it to the CTO for approval, then the code will be executed by the software engineer."
        "It always respond 'TERMINATE' when it's done.",
    )
    llm_config={"config_list": config_list}
)

software_engineer = autogen.AssistantAgent(
    name="Software_Engineer",
    system_message="A software engineer of the company, its responsibility is to develop the instructions given by the PM and generate python codes for develoing the project.",

)

groupchat = autogen.GroupChat(agents = [user_proxy, cto, pm, software_engineer], messages=[], max_round=12)
group_manager = autogen.GroupChatManager(
    system_message="A group chat manager. It never sends the message of a participant to itself.",
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)


user_proxy.initiate_chat(group_manager, message="Plan the backend for the authencitation system of a website")