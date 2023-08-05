
 #  Copyright 2019  Dialect Software LLC or its affiliates. All Rights Reserved.
 #
 #  Licensed under the MIT License (the "License").
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pylingo",
    version="0.0.3",
    author="Dialect Software LLC",
    author_email="support@dialectsoftware.com",
    description="General Purpose Configuration Language Framework",
    long_description="Pylingo is a framework for building a custom DSL(s)",
    long_description_content_type="text/markdown",
    url="https://github.com/dialectsoftware/pylingo",
    packages= find_packages(),
    install_requires=[
          'antlr4-python3-runtime'
      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)