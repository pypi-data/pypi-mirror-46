from anna_lib.selenium import events
from anna_lib.task.abstract_task import AbstractTask


class Empty(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.hover(self.driver, target='#minicart')
		events.click(self.driver, target='.viewcart')
		events.click(self.driver, target='#empty_cart_button')

	def after_execute(self):
		pass
