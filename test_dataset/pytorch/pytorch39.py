def test_list_sort(self):
        template = dedent('''
        def func():
            li_1 = {list_create}
            li_2 = {list_create}
            li_3 = {list_create}
            li_1.sort()
            li_2.sort(reverse=True)
            li_4 = sorted(li_3)
            return li_1, li_2, li_3, li_4
        ''')

        lists = ["[]", "[1, 3, 2]", "[True, False, True]", "[1.2, .2, 3.2]",
                 "[torch.tensor(1.0), torch.tensor(0.2), torch.tensor(0.5)]",
                 "[torch.tensor(5), torch.tensor(-2), torch.tensor(4)]"]
        for li in lists:
            code = template.format(list_create=li)
            scope = {}
            exec(code, globals(), scope)
            cu = torch.jit.CompilationUnit(code)
            t1 = cu.func()
            t2 = scope['func']()
            self.assertEqual(t1, t2)
