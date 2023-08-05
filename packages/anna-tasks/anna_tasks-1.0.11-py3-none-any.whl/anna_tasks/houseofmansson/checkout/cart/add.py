from anna_lib.selenium import events, util, assertions
from anna_lib.task.abstract_task import AbstractTask


class Add(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.click(self.driver, target='#search')
		events.send_keys(self.driver, target='#search', value='AB-WTNOTE009')
		events.submit(self.driver, target='#search')
		events.click(self.driver, target='a.product-item-photo')
		if util.get_element(self.driver, target='.required-entry'):
			events.click(self.driver, target='.required-entry')
			events.click(self.driver, target="$xpath//select[starts-with(@id, 'attribute')]/option[@value='1217']")
		events.click(self.driver, target='.tocart')

	def after_execute(self):
		self.result.append(assertions.element_exists(self.driver, target='.message-success'))
