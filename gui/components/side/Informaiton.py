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
            
            <h3>MIT License (for OpenAI)</h3>
            <p>Copyright (c) OpenAI</p>
            <p>
                Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
                documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
                the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
                and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
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
            <p>Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance 
                with the License. You may obtain a copy of the License at</p>
            <p><a href="http://www.apache.org/licenses/LICENSE-2.0">http://www.apache.org/licenses/LICENSE-2.0</a></p>
            <p>Unless required by applicable law or agreed to in writing, software distributed under the License is distributed 
                on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for 
                the specific language governing permissions and limitations under the License.
            </p>

            <hr>

            <h3>wxWindows Library License, Version 3.1 (for wxPython)</h3>
            <p>Copyright (c) 1998-2005 Julian Smart, Robert Roebling et al</p>
            <p>Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.</p>
            <p>This library is free software; you can redistribute it and/or modify it under the terms of the GNU Library General Public 
                License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.</p>
            <p>This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
                of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Library General Public License for more details.</p>
            <p>You should have received a copy of the GNU Library General Public License along with this library; if not, write to the Free 
                Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.</p>
            <p>An exception is herewith granted to link this library with independent modules to produce an executable, regardless of the license 
                terms of these independent modules, and to copy and distribute the resulting executable under terms of your choice, provided that you 
                also meet, for each linked independent module, the terms and conditions of the license of that module. An independent module is a 
                module which is not derived from or based on this library. If you modify this library, you may extend this exception to your version 
                of the library, but you are not obligated to do so. If you do not wish to do so, delete this exception statement from your version.
            </p>

            <hr>

            <h3>Apache License Version 2.0, January 2004 (for cryptography)</h3>
            <pre>
Apache License
Version 2.0, January 2004
https://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

    "License" shall mean the terms and conditions for use, reproduction,
    and distribution as defined by Sections 1 through 9 of this document.

    "Licensor" shall mean the copyright owner or entity authorized by
    the copyright owner that is granting the License.

    "Legal Entity" shall mean the union of the acting entity and all
    other entities that control, are controlled by, or are under common
    control with that entity. For the purposes of this definition,
    "control" means (i) the power, direct or indirect, to cause the
    direction or management of such entity, whether by contract or
    otherwise, or (ii) ownership of fifty percent (50%) or more of the
    outstanding shares, or (iii) beneficial ownership of such entity.

    "You" (or "Your") shall mean an individual or Legal Entity
    exercising permissions granted by this License.

    "Source" form shall mean the preferred form for making modifications,
    including but not limited to software source code, documentation
    source, and configuration files.

    "Object" form shall mean any form resulting from mechanical
    transformation or translation of a Source form, including but
    not limited to compiled object code, generated documentation,
    and conversions to other media types.

    "Work" shall mean the work of authorship, whether in Source or
    Object form, made available under the License, as indicated by a
    copyright notice that is included in or attached to the work
    (an example is provided in the Appendix below).

    "Derivative Works" shall mean any work, whether in Source or Object
    form, that is based on (or derived from) the Work and for which the
    editorial revisions, annotations, elaborations, or other modifications
    represent, as a whole, an original work of authorship. For the purposes
    of this License, Derivative Works shall not include works that remain
    separable from, or merely link (or bind by name) to the interfaces of,
    the Work and Derivative Works thereof.

    "Contribution" shall mean any work of authorship, including
    the original version of the Work and any modifications or additions
    to that Work or Derivative Works thereof, that is intentionally
    submitted to Licensor for inclusion in the Work by the copyright owner
    or by an individual or Legal Entity authorized to submit on behalf of
    the copyright owner. For the purposes of this definition, "submitted"
    means any form of electronic, verbal, or written communication sent
    to the Licensor or its representatives, including but not limited to
    communication on electronic mailing lists, source code control systems,
    and issue tracking systems that are managed by, or on behalf of, the
    Licensor for the purpose of discussing and improving the Work, but
    excluding communication that is conspicuously marked or otherwise
    designated in writing by the copyright owner as "Not a Contribution."

    "Contributor" shall mean Licensor and any individual or Legal Entity
    on behalf of whom a Contribution has been received by Licensor and
    subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
    this License, each Contributor hereby grants to You a perpetual,
    worldwide, non-exclusive, no-charge, royalty-free, irrevocable
    copyright license to reproduce, prepare Derivative Works of,
    publicly display, publicly perform, sublicense, and distribute the
    Work and such Derivative Works in Source or Object form.

3. Grant of Patent License. Subject to the terms and conditions of
    this License, each Contributor hereby grants to You a perpetual,
    worldwide, non-exclusive, no-charge, royalty-free, irrevocable
    (except as stated in this section) patent license to make, have made,
    use, offer to sell, sell, import, and otherwise transfer the Work,
    where such license applies only to those patent claims licensable
    by such Contributor that are necessarily infringed by their
    Contribution(s) alone or by combination of their Contribution(s)
    with the Work to which such Contribution(s) was submitted. If You
    institute patent litigation against any entity (including a
    cross-claim or counterclaim in a lawsuit) alleging that the Work
    or a Contribution incorporated within the Work constitutes direct
    or contributory patent infringement, then any patent licenses
    granted to You under this License for that Work shall terminate
    as of the date such litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the
    Work or Derivative Works thereof in any medium, with or without
    modifications, and in Source or Object form, provided that You
    meet the following conditions:

    (a) You must give any other recipients of the Work or
        Derivative Works a copy of this License; and

    (b) You must cause any modified files to carry prominent notices
        stating that You changed the files; and

    (c) You must retain, in the Source form of any Derivative Works
        that You distribute, all copyright, patent, trademark, and
        attribution notices from the Source form of the Work,
        excluding those notices that do not pertain to any part of
        the Derivative Works; and

    (d) If the Work includes a "NOTICE" text file as part of its
        distribution, then any Derivative Works that You distribute must
        include a readable copy of the attribution notices contained
        within such NOTICE file, excluding those notices that do not
        pertain to any part of the Derivative Works, in at least one
        of the following places: within a NOTICE text file distributed
        as part of the Derivative Works; within the Source form or
        documentation, if provided along with the Derivative Works; or,
        within a display generated by the Derivative Works, if and
        wherever such third-party notices normally appear. The contents
        of the NOTICE file are for informational purposes only and
        do not modify the License. You may add Your own attribution
        notices within Derivative Works that You distribute, alongside
        or as an addendum to the NOTICE text from the Work, provided
        that such additional attribution notices cannot be construed
        as modifying the License.

    You may add Your own copyright statement to Your modifications and
    may provide additional or different license terms and conditions
    for use, reproduction, or distribution of Your modifications, or
    for any such Derivative Works as a whole, provided Your use,
    reproduction, and distribution of the Work otherwise complies with
    the conditions stated in this License.

5. Submission of Contributions. Unless You explicitly state otherwise,
    any Contribution intentionally submitted for inclusion in the Work
    by You to the Licensor shall be under the terms and conditions of
    this License, without any additional terms or conditions.
    Notwithstanding the above, nothing herein shall supersede or modify
    the terms of any separate license agreement you may have executed
    with Licensor regarding such Contributions.

6. Trademarks. This License does not grant permission to use the trade
    names, trademarks, service marks, or product names of the Licensor,
    except as required for reasonable and customary use in describing the
    origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or
    agreed to in writing, Licensor provides the Work (and each
    Contributor provides its Contributions) on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied, including, without limitation, any warranties or conditions
    of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
    PARTICULAR PURPOSE. You are solely responsible for determining the
    appropriateness of using or redistributing the Work and assume any
    risks associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory,
    whether in tort (including negligence), contract, or otherwise,
    unless required by applicable law (such as deliberate and grossly
    negligent acts) or agreed to in writing, shall any Contributor be
    liable to You for damages, including any direct, indirect, special,
    incidental, or consequential damages of any character arising as a
    result of this License or out of the use or inability to use the
    Work (including but not limited to damages for loss of goodwill,
    work stoppage, computer failure or malfunction, or any and all
    other commercial damages or losses), even if such Contributor
    has been advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing
    the Work or Derivative Works thereof, You may choose to offer,
    and charge a fee for, acceptance of support, warranty, indemnity,
    or other liability obligations and/or rights consistent with this
    License. However, in accepting such obligations, You may act only
    on Your own behalf and on Your sole responsibility, not on behalf
    of any other Contributor, and only if You agree to indemnify,
    defend, and hold each Contributor harmless for any liability
    incurred by, or claims asserted against, such Contributor by reason
    of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

APPENDIX: How to apply the Apache License to your work.

    To apply the Apache License to your work, attach the following
    boilerplate notice, with the fields enclosed by brackets "[]"
    replaced with your own identifying information. (Don't include
    the brackets!)  The text should be enclosed in the appropriate
    comment syntax for the file format. We also recommend that a
    file or class name and description of purpose be included on the
    same "printed page" as the copyright notice for easier
    identification within third-party archives.

    Copyright [yyyy] [name of copyright owner]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
            </pre>

            <hr>

            <h3>Used for Distribution</h3>

            <h3>PyInstaller License Information</h3>
            <p>This project uses PyInstaller to package the application into an executable format.</p>
            <p>PyInstaller is licensed under the GNU General Public License (GPL) version 2 (or later), with a special exception for the bootloader. 
            This exception permits the distribution of executables created with PyInstaller without applying the full terms of the GPL to the 
            entire application.</p>
            <h4>Bootloader Exception:</h4>
            <p>The authors of PyInstaller grant you unlimited permission to link or embed the compiled bootloader and related files into combinations 
                with other programs, and to distribute those combinations without any restriction coming from the use of those files. However, the 
                General Public License restrictions still apply to the PyInstaller code itself, particularly when it is not linked into a combined 
                executable.</p>
            <p>For more information, please refer to:</p>
            <ul>
                <li>GNU GPL v2 License: <a href="https://www.gnu.org/licenses/gpl-2.0.html">https://www.gnu.org/licenses/gpl-2.0.html</a></li>
                <li>PyInstaller documentation: <a href="https://www.pyinstaller.org/">https://www.pyinstaller.org/</a></li>
            </ul>
            <p>In summary, executables generated using PyInstaller can be freely distributed without requiring the entire project to comply with the full 
            terms of GPLv2.</p>
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
