from interfaces.controllers.project_controller import CreateProjectHandler
from interfaces.controllers.routing_controller import InsertTemplateRoutingHandler
from interfaces.controllers.verification_controller import VerificationAssemSPHandler


def setup_signals(main_window):
    main_window.button_create_project.clicked.connect(
        lambda: CreateProjectHandler(main_window).handle()
    )

    main_window.button_paste_template_routing.clicked.connect(
        lambda: InsertTemplateRoutingHandler(main_window).handle()
    )

    main_window.button_verification_project.clicked.connect(
        lambda: VerificationAssemSPHandler(main_window).handle()
    )
