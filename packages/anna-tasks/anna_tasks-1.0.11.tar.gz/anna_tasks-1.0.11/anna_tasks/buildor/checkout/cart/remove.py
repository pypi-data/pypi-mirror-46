from anna_lib.selenium import assertions, events, util
from anna_lib.task.abstract_task import AbstractTask


class Remove(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.hover(self.driver, target='#search')
		if util.get_element(self.driver, target='.btn-remove'):
			events.click(self.driver, target='.btn-remove')

	def after_execute(self):
		pass
