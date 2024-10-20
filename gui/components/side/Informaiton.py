import wx
import wx.html
import webbrowser


class Information(wx.Dialog):
    def __init__(self, parent, title="Information"):
        super().__init__(parent, title=title, size=(700, 600))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 라이선스 HTML 텍스트
        license_html = """
        <html>
        <body>
            <h1>MIT License</h1>
            <p>Copyright (c) 2024 CBNU-SUPER-NOVA</p>
            <p>
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
                documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
                the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
                and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            </p>
            <p>
                The above copyright notice and this permission notice shall be included in all copies or substantial portions 
                of the Software.
            </p>
            <p>
                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
                THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
                TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
                SOFTWARE.
            </p>

            <hr>

            <h2>Third-Party Licenses</h2>
            
            <h3>MIT License (for OpenAI and python-dotenv)</h3>
            <p>Copyright (c) OpenAI<br>
            Copyright (c) 2014, Saurabh Kumar (python-dotenv), 2013, Ted Tieken (django-dotenv-rw), 2013, Jacob Kaplan-Moss (django-dotenv)</p>
            <p>
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
                documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
                the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
                and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            </p>
            <p>
                The above copyright notice and this permission notice shall be included in all copies or substantial portions 
                of the Software.
            </p>
            <p>
                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
                THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
                TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
                SOFTWARE.
            </p>

            <hr>

            <h3>Apache License 2.0 (for google-generativeai)</h3>
            <p>Copyright (c) Google LLC</p>
            <p>
                Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance 
                with the License. You may obtain a copy of the License at
            </p>
            </a>http://www.apache.org/licenses/LICENSE-2.0</a>
            <p>
                Unless required by applicable law or agreed to in writing, software distributed under the License is distributed 
                on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for 
                the specific language governing permissions and limitations under the License.
            </p>

            <hr>

            <h3>wxWindows Library License, Version 3.1 (for wxPython)</h3>
            <p>Copyright (c) 1998-2005 Julian Smart, Robert Roebling et al</p>
            <p>
                Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.
            </p>
            <p>
                This library is free software; you can redistribute it and/or modify it under the terms of the GNU Library General Public 
                License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
            </p>
            <p>
                This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
                of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Library General Public License for more details.
            </p>
            <p>
                You should have received a copy of the GNU Library General Public License along with this library; if not, write to the Free 
                Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
            </p>
            <p>
                An exception is herewith granted to link this library with independent modules to produce an executable, regardless of the license 
                terms of these independent modules, and to copy and distribute the resulting executable under terms of your choice, provided that you 
                also meet, for each linked independent module, the terms and conditions of the license of that module. An independent module is a 
                module which is not derived from or based on this library. If you modify this library, you may extend this exception to your version 
                of the library, but you are not obligated to do so. If you do not wish to do so, delete this exception statement from your version.
            </p>

            <hr>

            <h3>PyInstaller License Information</h3>
            <p>
                This project uses PyInstaller to package the application into an executable format.
            </p>
            <p>
                PyInstaller is licensed under the GNU General Public License (GPL) version 2 (or later), with a special exception for the bootloader. 
                This exception permits the distribution of executables created with PyInstaller without applying the full terms of the GPL to the 
                entire application.
            </p>
            <h4>Bootloader Exception:</h4>
            <p>
                The authors of PyInstaller grant you unlimited permission to link or embed the compiled bootloader and related files into combinations 
                with other programs, and to distribute those combinations without any restriction coming from the use of those files. However, the 
                General Public License restrictions still apply to the PyInstaller code itself, particularly when it is not linked into a combined 
                executable.
            </p>
            <p>For more information, please refer to:</p>
            <ul>
                <li>GNU GPL v2 License: <a href="https://www.gnu.org/licenses/gpl-2.0.html">https://www.gnu.org/licenses/gpl-2.0.html</a></li>
                <li>PyInstaller documentation: <a href="https://www.pyinstaller.org/">https://www.pyinstaller.org/</a></li>
            </ul>
            <p>
                In summary, executables generated using PyInstaller can be freely distributed without requiring the entire project to comply with the full 
                terms of GPLv2.
            </p>
        </body>
        </html>
        """

        # HTML 보기 컨트롤
        html_window = wx.html.HtmlWindow(panel, size=(700, 500))
        html_window.SetPage(license_html)

        # 링크 클릭 이벤트 바인딩
        html_window.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_link_clicked)

        vbox.Add(html_window, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # OK 버튼
        ok_button = wx.Button(panel, label='OK')
        ok_button.Bind(wx.EVT_BUTTON, self.on_close)
        vbox.Add(ok_button, flag=wx.ALL | wx.CENTER, border=10)

        panel.SetSizer(vbox)

    def on_link_clicked(self, event):
        """사용자가 링크를 클릭했을 때 웹 브라우저에서 열림"""
        url = event.GetLinkInfo().GetHref()
        webbrowser.open(url)  # 기본 웹 브라우저에서 링크 열기

    def on_close(self, event):
        self.Close()
