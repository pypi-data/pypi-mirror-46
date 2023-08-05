from anna_lib.selenium import assertions, events, util
from anna_lib.task.abstract_task import AbstractTask


class Add(AbstractTask):
	def before_execute(self):
		pass

	def __execute__(self):
		events.click(self.driver, target='#search')
		events.send_keys(self.driver, target='#search', value='XA-123')
		events.submit(self.driver, target='#search')
		events.click(self.driver, target='a.product-image')
		if util.get_element(self.driver, target='.required-entry'):
			events.click(self.driver, target='.required-entry')
			events.click(self.driver, target="$xpath//select[starts-with(@id, 'attribute')]/option[@value='1217']")
		events.click(self.driver, target='.add-to-cart')

	def after_execute(self):
		self.result.append(assertions.url_equals(self.driver, expected='https://www.buildor.se/checkout/cart/'))
