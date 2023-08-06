from vigo.github import Github


class Analyze(object):
    """To analyze the file."""

    def __init__(self, groups, governance, query):
        """Initialize an analyze."""
        self.github = Github()
        self.groups = groups
        self.gov = governance
        self.query = query
        self.projects = []
        self.get_projects()
        self.result = self.github.search(query, self.projects)
        self.extract_result()

    def get_repos(self, group, project):
        return self.gov.config[group]["deliverables"][project]["repos"][0]

    def get_projects(self):
        for group in self.gov.config:
            if group not in self.groups:
                continue
            try:
                projects = [
                    self.get_repos(group, project)
                    for project in self.gov.config[group]["deliverables"]
                ]
            except KeyError:
                continue
            finally:
                self.projects.extend(projects)

    def extract_result(self):
        summary = "{count} results found".format(
            count=self.result["total_count"]
        )
        sorted_results = {}
        print(summary)
        print("~" * len(summary))
        for item in self.result["items"]:
            repo = item["repository"]["full_name"]
            if repo not in sorted_results:
                sorted_results.update({repo: []})

            sorted_results[repo].append(
                "{path} ({sha})".format(path=item["path"], sha=item["sha"])
            )
        for el in sorted_results:
            print(el)
            for res in sorted_results[el]:
                print(res)
