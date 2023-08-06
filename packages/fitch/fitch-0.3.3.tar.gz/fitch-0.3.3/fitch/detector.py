"""
MIT License

Copyright (c) 2018 williamfzc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json

from findit import FindIt

from fitch import config
from fitch.logger import logger

TEMP_TEMPLATE_NAME = 'cur_template'
TEMP_TARGET_NAME = 'cur_target'

fi = FindIt(
    engine=['template'],
    engine_template_cv_method_name=config.CV_METHOD_NAME,
    engine_template_scale=config.CV_PIC_SCALE,
    pro_mode=True,
)


def detect(template: str, target: str) -> dict:
    # load template picture
    fi.load_template(TEMP_TEMPLATE_NAME, pic_path=template)
    # and find it
    result = fi.find(TEMP_TARGET_NAME, target_pic_path=target)
    fi.clear()
    logger.debug('Detect result: {}'.format(json.dumps(result)))
    return result


def cal_location(result_dict: dict) -> (list, tuple):
    """ analyse result and get its position """
    result_dict = result_dict['data'][TEMP_TEMPLATE_NAME]['TemplateEngine']
    target_point = result_dict['target_point']
    target_sim = result_dict['target_sim']
    assert target_sim > config.CV_THRESHOLD, 'target point not found'
    logger.info('Similarity: {}. Target found: ({}, {})'.format(target_sim, *target_point))
    return target_point


if __name__ == '__main__':
    res = detect('../point.png', '../screen.png')
    print(res)
