# -*- coding: utf-8 -*-
import re
from slugify import slugify


QUOTE_PATTERN = re.compile(r'[\']+')


def generate_slug(book_title, *other_titles):
    """Generates a slug for a book title or a section title.

    GIVEN just the book title
    book_title = "College Physics"
    RETURNS
     "college-physics"

    GIVEN
    book_title = "College Physics"
    other_title = "1.1 The Science of Biology"
    RETURNS
     "1-1-the-science-of-biology"

     GIVEN
     book_title = "College Physics"
     other_title[0] = "1 Introduction: The Nature of Science and Physics"
     other_title[1] = "Problems &amp; Exercises"
     RETURNS
     "1-problems-exercises"

     NOTE that the chapter title is only used to determine the chapter number
     in case it is missing from the section title - like for "Introduction" sections.
    """
    if len(other_titles) == 0:
        book_title = slugify(remove_html_tags(book_title))
        return book_title

    section_title = other_titles[-1]
    # Remove any quotes from the textp
    section_title = QUOTE_PATTERN.sub('', section_title)

    section_title = slugify(remove_html_tags(section_title))

    if re.match(r"^\d", section_title):  # if section title starts with a digit
        # we must already have the chapter and section numbers
        return section_title
    else:  # find the chapter number
        try:
            chapter_title = remove_html_tags(other_titles[-2])
            chapter_number = re.split(r"^([0-9\.]*)?(.*)$", chapter_title)[1]
            section_title = "{}-{}".format(chapter_number, section_title) if chapter_number else section_title
        except IndexError:
            pass  # chapter title not present

        return section_title


def remove_html_tags(title):
    return re.sub(r"<.*?>", "", title)
