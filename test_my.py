from selenium import webdriver
from selenium.webdriver.common.by import By
from subprocess import Popen
import time
import unittest


class MainTestClass(unittest.TestCase):
    BACKEND_NAME = 'backend.py'
    START_URL = 'http://localhost:8001'
    LOGOUT_SIGNATURE = 'Log Out'

    def setUp(self):
        self.backend_process = Popen(['python', self.BACKEND_NAME])

    def tearDown(self):
        self.backend_process.kill()

    def _log_in(self, driver, email, password):
        elem = driver.find_element(By.NAME, 'email')
        elem.clear()
        elem.send_keys(email)

        elem = driver.find_element(By.NAME, 'password')
        elem.clear()
        elem.send_keys(password)
        driver.find_element(By.XPATH, '//button[.="Log In"]').click()

    def _post_comment(self, driver, text_comment):
        driver.find_element(By.CLASS_NAME, 'ql-editor').clear()
        driver.find_element(By.CLASS_NAME, 'ql-editor').send_keys(text_comment)
        driver.find_element(By.XPATH, '//button[.="New comment"]').click()

    def test_task1(self):
        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)

            elem = driver.find_elements(By.XPATH, '//h1[.="Is this a good way to process input?"]')
            self.assertTrue(elem, 'Question header is absent')

            elem = driver.find_elements(By.XPATH, '//div[@id="question"]/pre[text()!=""]')
            self.assertTrue(elem, 'Question body is empty')

            comments = (
                ('Test comment 1', 'Alice A.'),
                ('Test comment 2', 'Bob B.'),
            )

            for comment, elem in zip(comments, driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li')):
                comment_text = elem.find_element(By.TAG_NAME, 'span').text
                author = elem.find_element(By.TAG_NAME, 'a').text
                self.assertEqual(comment, (comment_text, author), 'Comment does not match')

            elem = driver.find_elements(By.XPATH, '//button[.="Sign Up"]')
            self.assertTrue(elem, 'Sign up button is missing')

            elem = driver.find_elements(By.XPATH, '//button[.="Log In"]')
            self.assertTrue(elem, 'Log in button is missing')

            elem = driver.find_elements(By.XPATH, '//div[input[@name="display_name"]]')
            self.assertTrue(elem, 'There is no field for entering a Display name')

            elem = driver.find_elements(By.XPATH, '//div[input[@name="email"]]')
            self.assertTrue(elem, 'There is no field for entering an Email')

            elem = driver.find_elements(By.XPATH, '//div[input[@name="password"]]')
            self.assertTrue(elem, 'There is no field for entering a Password')

            time.sleep(5)

    def test_task2(self):
        display_name = 'Cavin C.'
        email = 'cavin@gmail.com'
        password = 'ccc'

        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)

            driver.find_element(By.NAME, 'display_name').send_keys(display_name)
            driver.find_element(By.NAME, 'email').send_keys(email)
            driver.find_element(By.NAME, 'password').send_keys(password)
            driver.find_element(By.XPATH, '//button[.="Sign Up"]').click()

            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(raw_text[:-len(self.LOGOUT_SIGNATURE)], display_name)

            driver.find_element(By.XPATH, '//button[.="Log Out"]').click()
            elems = driver.find_elements(By.XPATH, '//button[.="Log In"]')
            self.assertTrue(elems, 'User did not log out')

            other_display_name = 'Bella B.'
            elem = driver.find_element(By.NAME, 'display_name')
            elem.clear()
            elem.send_keys(other_display_name)

            elem = driver.find_element(By.NAME, 'email')
            elem.clear()
            elem.send_keys(email)

            elem = driver.find_element(By.NAME, 'password')
            elem.clear()
            elem.send_keys(password)

            driver.find_element(By.XPATH, '//button[.="Sign Up"]').click()

            elems = driver.find_elements(By.XPATH, '//button[.="Log Out"]')
            self.assertFalse(elems, 'User actually logged in with non unique email')

            time.sleep(5)

    def test_task3(self):
        email, password = 'alice_2002@gmail.com', 'aaa'

        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self.assertTrue(driver.find_elements(By.XPATH, '//button[.="Log Out"]'))
            raw_text = driver.find_element(By.ID, 'signup-section').text
            self.assertEqual(raw_text[:-len(self.LOGOUT_SIGNATURE)], 'Alice A.')

    def test_task4(self):
            email, password = 'alice_2002@gmail.com', 'aaa'
            my_script = """
            var elem = document.getElementById('editor-section');
            elem.style.borderColor = "red";
            elem.style.borderStyle = "solid";
            """

            driver = webdriver.Chrome()
            with driver:
                driver.get(self.START_URL)
                self._log_in(driver, email, password)

                elem = driver.find_element(By.ID, 'editor-section')
                self.assertTrue(elem, 'Editor section is not present')
                elem = driver.find_element(By.XPATH, '//button[.="New comment"]')
                self.assertTrue(elem, 'New comment button is missing')

                driver.execute_script(my_script)
                driver.save_screenshot('my_screeen.png')


    def test_task5(self):
        def click_style(style_name):
            driver.find_element(By.CLASS_NAME, 'ql-' + style_name).click()

        email, password = 'alice_2002@gmail.com', 'aaa'
        my_comment = 'Comment from Alice'
        expected_formatted_comment_html = '<span><u>Comment</u> from Alice</span>'

        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self._post_comment(driver, my_comment)
            xp = '//div[@id="comments"]/ul/li[last()][span="{}"][a="Alice A."][span/button="Remove"]'.format(my_comment)
            self.assertTrue(driver.find_element(By.XPATH, xp), 'New comment is not correct')

            driver.find_element(By.CLASS_NAME, 'ql-editor').clear()
            elem = driver.find_element(By.CLASS_NAME, 'ql-editor')
            click_style('underline')
            elem.send_keys('Comment')
            click_style('underline')
            elem.send_keys(' from Alice')
            driver.find_element(By.XPATH, '//button[.="New comment"]').click()

            elem = driver.find_element(By.XPATH, '//div[@id="comments"]/ul/li[last()]/span')
            extracted_html = elem.get_attribute('outerHTML')
            self.assertEqual(extracted_html, expected_formatted_comment_html)

            #italic
        expected_formatted_comment_html = '<span><em>Comment</em> from Alice</span>'
        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self._post_comment(driver, my_comment)
            xp = '//div[@id="comments"]/ul/li[last()][span="{}"][a="Alice A."][span/button="Remove"]'.format(my_comment)
            self.assertTrue(driver.find_element(By.XPATH, xp), 'New comment is not correct')

            driver.find_element(By.CLASS_NAME, 'ql-editor').clear()
            elem = driver.find_element(By.CLASS_NAME, 'ql-editor')
            click_style('italic')
            elem.send_keys('Comment')
            click_style('italic')
            elem.send_keys(' from Alice')
            driver.find_element(By.XPATH, '//button[.="New comment"]').click()

            elem = driver.find_element(By.XPATH, '//div[@id="comments"]/ul/li[last()]/span')
            extracted_html = elem.get_attribute('outerHTML')
            self.assertEqual(extracted_html, expected_formatted_comment_html)


    def test_task6(self):
        email, password = 'alice_2002@gmail.com', 'aaa'
        my_comment1 = 'aaaaaaaaaaaaaaaaaaa'
        my_comment2 = 'AAAAAAAAAAAAAAAAAAA'

        driver = webdriver.Chrome()
        with driver:
            driver.get(self.START_URL)
            self._log_in(driver, email, password)

            self._post_comment(driver, my_comment1)
            xp = '//div[@id="comments"]/ul/li[last()][span="{}"][a="Alice A."][span/button="Remove"]'.format(
                my_comment1)
            self.assertTrue(driver.find_element(By.XPATH, xp), 'New comment is not correct')

            self._post_comment(driver, my_comment2)
            xp = '//div[@id="comments"]/ul/li[last()][span="{}"][a="Alice A."][span/button="Remove"]'.format(
                my_comment2)
            self.assertTrue(driver.find_element(By.XPATH, xp), 'New comment is not correct')

    def test_task7(self):

        display_name,existing_email, existing_password = 'Alice A.', 'alice_2002@gmail.com', 'aaa'
        driver = webdriver.Chrome()
        with driver:
            #a.	Переконатися, що видаляється потрібний коментар.
            # b.	Переконатися, що усі інші коментарі, створені даним користувачем та іншими користувачами, залишилися на місці.
            driver.get(self.START_URL)
            self._log_in(driver, existing_email, existing_password)
            count_comments_old = driver.find_elements_by_xpath(f'//div[@id="comments"]/ul/li')
            all_comments = driver.find_elements_by_xpath(
                f'//div[@id="comments"]/ul/li[a = "{display_name}"]/span[1]')
            users_comments_text = [comment.text for comment in all_comments]
            del_comm = users_comments_text[0]

            remove_1_comm_button = driver.find_elements_by_xpath(f'//div[@id="comments"]/ul/li[span="{del_comm}"][a="{display_name}"]/span/button[.="Remove"]')[0]
            remove_1_comm_button.click()

            count_comments_new = driver.find_elements_by_xpath(f'//div[@id="comments"]/ul/li')
            self.assertEqual(len(count_comments_new), len(count_comments_old) - 1, 'Problems in deleting comment')

    def test_task8(self):
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        another_driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        with driver as driver1:
            driver1.get(self.START_URL)
            inpt1 = driver1.find_element_by_xpath('//input[@name="display_name"]')
            inpt1.send_keys("user1")
            inpt2 = driver1.find_element_by_xpath('//input[@name="email"]')

            inpt2.send_keys("user1@gmail.com")
            inpt3 = driver1.find_element_by_xpath('//input[@name="password"]')

            inpt3.send_keys("111")
            time.sleep(1)
            driver1.find_element_by_xpath('//button[.="Sign Up"]').click()
            time.sleep(1)
            field = driver1.find_element_by_xpath('//div[@class="ql-container ql-snow"]/div/p[.="(enter new comment)"]')
            field.clear()
            comment1_txt = "comment1"
            driver1.find_element_by_xpath('//div[@class="ql-container ql-snow"]/div').send_keys(comment1_txt)
            driver1.find_element_by_xpath('//button[.="New comment"]').click()
            time.sleep(2)
            with another_driver as driver_test:
                driver_test.get(self.START_URL)
                inpt1 = driver_test.find_element_by_xpath('//input[@name="display_name"]')
                inpt1.clear()
                inpt1.send_keys("user2")
                inpt2 = driver_test.find_element_by_xpath('//input[@name="email"]')
                inpt2.clear()
                inpt2.send_keys("user2@gmail.com")
                inpt3 = driver_test.find_element_by_xpath('//input[@name="password"]')
                inpt3.clear()
                inpt3.send_keys("222")
                time.sleep(1)
                driver_test.find_element_by_xpath('//button[.="Sign Up"]').click()
                time.sleep(1)
                field = driver_test.find_element_by_xpath(
                    '//div[@class="ql-container ql-snow"]/div/p[.="(enter new comment)"]')
                field.clear()
                comment2_txt = "comment2"
                driver_test.find_element_by_xpath('//div[@class="ql-container ql-snow"]/div').send_keys(comment2_txt)
                driver_test.find_element_by_xpath('//button[.="New comment"]').click()
                time.sleep(3)
                lst_comments = list()
                lst_comments.append(comment1_txt)
                lst_comments.append(comment2_txt)
                index_lst = [-2, -1]
                path_page_comments = driver_test.find_elements_by_xpath('//div[@id="comments"]/ul/li/span[1]')
                lst_page_comments = [path_page_comments[i].get_attribute("innerHTML") for i in index_lst]
                self.assertListEqual(lst_page_comments, lst_comments, "Comment structure was broken")

        time.sleep(5)

if __name__ == '__main__':
    unittest.main()
