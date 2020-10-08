resource "aws_alb" "python-alb" {
  name            = "python-alb"
  subnets         = aws_subnet.public.*.id
  security_groups = [aws_security_group.python-alb-sg.id]
}

resource "aws_alb_target_group" "python-server" {
  name        = "python-server"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.python-vpc.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "5"
    path                = "/"
    unhealthy_threshold = "2"
  }
}

resource "aws_alb_listener" "python-listener" {
  load_balancer_arn = aws_alb.python-alb.id
  port              = 5000
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.python-server.id
  }
}
