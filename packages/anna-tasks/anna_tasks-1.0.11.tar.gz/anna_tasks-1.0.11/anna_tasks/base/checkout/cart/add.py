from anna_lib.selenium import assertions, events
from anna_lib.task.abstract_task import AbstractTask


class Add(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.click(self.driver, target='#search')
		events.send_keys(self.driver, target='#search', value='Cassia Funnel Sweatshirt')
		events.submit(self.driver, target='#search')
		events.click(self.driver, target='.tocart')

	def after_execute(self):
		self.result.append(assertions.element_exists(self.driver, target='.message-success'))
