import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class KubeSecurityCrew():
	"""KubeSecurityCrew crew"""
	mistral_llm = LLM(
		model=os.environ.get('MISTRAL_MODEL'),#os.getenv("MISTRAL_MODEL"),
		max_new_tokens=16000,
		decoding_method="greedy",
	)

	# granite_llm = LLM(
	# 	model=os.getenv("GRANITE_MODEL"),
	# 	max_new_tokens=4000,
	# 	decoding_method="greedy",
	# )

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def security_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['security_analyst'],
			verbose=True,
			llm=self.mistral_llm,
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
	def security_scanner_task(self) -> Task:
		return Task(
			config=self.tasks_config['security_scanner_task'],
			tools=[SerperDevTool()]
		)

	@task
	def reviewer_task(self) -> Task:
		return Task(
			config=self.tasks_config['reviewer_task'],
			#output_file='report.md'
			#tools=[SerperDevTool()],
			context=[self.security_scanner_task()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the KubeSecurityCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
