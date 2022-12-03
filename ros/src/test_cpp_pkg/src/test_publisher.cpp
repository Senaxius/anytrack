#include "example_interfaces/msg/string.hpp"
#include "rclcpp/rclcpp.hpp"

class test_publisher : public rclcpp::Node  // MODIFY NAME
{
   public:
    test_publisher() : Node("test_publisher"), name_("Björn")  // MODIFY NAME
    {
        publisher_ = this->create_publisher<example_interfaces::msg::String>("test_publisher", 10);
        timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&test_publisher::publish, this));

        RCLCPP_INFO(this->get_logger(), "cpp test_publisher has been started...");
    }

   private:
    void publish() {
        auto msg = example_interfaces::msg::String();
        msg.data = std::string("Hello, I'm ") + name_;
        publisher_->publish(msg);
    }

    std::string name_;
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<test_publisher>();  // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}