import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class KubeChatterCrew():
    """KubeChatterCrew crew"""
    mistral_llm = LLM(
        model=os.environ.get('MISTRAL_MODEL'),#os.getenv("MISTRAL_MODEL"),
        max_new_tokens=16000,
        decoding_method="greedy",
    )

    granite_llm = LLM(
        model=os.environ.get('GRANITE_MODEL'),# os.getenv("GRANITE_MODEL"),
        max_new_tokens=4000,
        decoding_method="greedy",
    )

    # k8siodocs_search_tool = WebsiteSearchTool(
    #     website="https://kubernetes.io/",
    #     config=dict(
    #         llm=dict(
    #             provider="ollama",  # or google, openai, anthropic, llama2, ...
    #             config=dict(
    #                 model="mxbai-embed-large",
    #                 base_url="http://9.30.79.188:11434",
    #                 # temperature=0.5,
    #                 # top_p=1,
    #                 # stream=true,
    #             ),
    #         ),
    #         embedder=dict(
    #             provider="ollama",  # or openai, ollama, ...
    #             config=dict(
    #                 model="mxbai-embed-large",
    #                 base_url="http://9.30.79.188:11434",
    #                 # title="Embeddings",
    #             ),
    #         ),
    #     )
    # )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'],
            verbose=True,
            llm=self.granite_llm,
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True,
            llm=self.mistral_llm,
        )

        # To learn more about structured task outputs,
        # task dependencies, and task callbacks, check out the documentation:
        # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def question_task(self) -> Task:
        return Task(
            config=self.tasks_config['question_task'],
            #    tools=[self.k8siodocs_search_tool]
        )

    @task
    def reviewer_task(self) -> Task:
        return Task(
            config=self.tasks_config['reviewer_task'],
            # tools=[SerperDevTool()],
            context=[self.question_task()]
            # output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the KubeChatterCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
